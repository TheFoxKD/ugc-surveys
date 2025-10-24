from dataclasses import dataclass
from datetime import timedelta
from typing import Final

from django.contrib.auth import get_user_model
from django.utils import timezone

from src.surveys.models import AnswerOption, Question, Survey, SurveyRun, UserAnswer
from src.users.enums import IdentityProvider
from src.users.models import Identity

User = get_user_model()


@dataclass(frozen=True)
class DemoSeedResult:
    author_email: str
    user_email: str
    password: str
    survey_id: int
    questions_created: int
    options_created: int
    run_id: int | None
    answers_created: int


class DemoSeedService:
    """Create a tiny, reusable demo dataset.

    The data is idempotent by unique emails and survey title.
    """

    AUTHOR_EMAIL: Final[str] = "demo.author@example.com"
    USER_EMAIL: Final[str] = "demo.user@example.com"
    PASSWORD: Final[str] = "Password123!"  # noqa: S105 - password is hardcoded for demo
    SURVEY_TITLE: Final[str] = "Демо опрос"

    @classmethod
    def seed(cls) -> DemoSeedResult:
        author = cls._get_or_create_user(cls.AUTHOR_EMAIL, is_staff=True)
        user = cls._get_or_create_user(cls.USER_EMAIL, is_staff=False)

        survey, _ = Survey.objects.get_or_create(
            title=cls.SURVEY_TITLE,
            defaults={"author": author},
        )

        questions_created = cls._ensure_questions(survey)
        options_created = cls._ensure_options(survey)

        run_id, answers_created = cls._ensure_completed_run(user, survey)

        return DemoSeedResult(
            author_email=cls.AUTHOR_EMAIL,
            user_email=cls.USER_EMAIL,
            password=cls.PASSWORD,
            survey_id=int(survey.id),
            questions_created=questions_created,
            options_created=options_created,
            run_id=run_id,
            answers_created=answers_created,
        )

    @classmethod
    def _get_or_create_user(cls, email: str, *, is_staff: bool) -> User:
        # Username is technical; email identity is stored in a separate model
        user, created = User.objects.get_or_create(
            username=email,  # keep deterministic to avoid duplicates
            defaults={"is_staff": is_staff},
        )
        if created:
            user.set_password(cls.PASSWORD)
            user.save(update_fields=["password"])
        Identity.objects.get_or_create(
            user=user,
            provider=IdentityProvider.EMAIL,
            value=email,
        )
        return user

    @classmethod
    def _ensure_questions(cls, survey: Survey) -> int:
        created = 0
        base = [
            (1, "Ты любишь помидоры?"),
            (2, "Ты любишь огурцы?"),
            (3, "Ты любишь буратту?"),
        ]
        for position, text in base:
            _, was_created = Question.objects.get_or_create(
                survey=survey,
                position=position,
                defaults={"text": text},
            )
            if was_created:
                created += 1
        return created

    @classmethod
    def _ensure_options(cls, survey: Survey) -> int:
        created = 0
        qs = Question.objects.filter(survey=survey)
        for q in qs:
            for position, text in ((1, "Да"), (2, "Нет"), (3, "Иногда")):
                _, was_created = AnswerOption.objects.get_or_create(
                    question=q,
                    position=position,
                    defaults={"text": text},
                )
                if was_created:
                    created += 1
        return created

    @classmethod
    def _ensure_completed_run(
        cls,
        user: User,
        survey: Survey,
    ) -> tuple[int | None, int]:
        # if a finished run exists, do not duplicate
        existing = (
            SurveyRun.objects.filter(user=user, survey=survey)
            .order_by("-started_at")
            .first()
        )
        if existing and existing.finished_at is not None:
            answers_count = UserAnswer.objects.filter(run=existing).count()
            return (int(existing.id), int(answers_count))

        run = SurveyRun.objects.create(
            user=user,
            survey=survey,
            started_at=timezone.now() - timedelta(minutes=1),
        )
        answers_created = 0
        for q in Question.objects.filter(survey=survey).order_by("position"):
            option = (
                AnswerOption.objects.filter(question=q).order_by("position").first()
            )
            if option is None:
                continue
            UserAnswer.objects.get_or_create(
                run=run,
                question=q,
                defaults={"selected_option": option},
            )
            answers_created += 1
        run.finished_at = run.started_at + timedelta(seconds=30)
        run.save(update_fields=["finished_at"])
        return (int(run.id), answers_created)
