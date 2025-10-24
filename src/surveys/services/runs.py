from django.db import transaction
from rest_framework.exceptions import ValidationError

from src.surveys.models import AnswerOption, Question, Survey, SurveyRun, UserAnswer
from src.users.models.user import User


class SurveyRunService:
    """Операции вокруг прохождения опроса."""

    @staticmethod
    def get_or_create_active_run(*, survey: Survey, user: User) -> SurveyRun:
        run, _created = SurveyRun.objects.get_or_create(
            user=user,
            survey=survey,
            finished_at__isnull=True,
        )
        return run

    @staticmethod
    def next_question(run: SurveyRun) -> Question | None:
        answered_ids = run.answers.values_list("question_id", flat=True)
        return (
            run.survey.questions.exclude(id__in=answered_ids)
            .order_by("position")
            .prefetch_related("answer_options")
            .first()
        )

    @staticmethod
    def is_completed(run: SurveyRun) -> bool:
        total_questions = run.survey.questions.count()
        answered_count = run.answers.count()
        return answered_count >= total_questions

    @staticmethod
    @transaction.atomic
    def create_answer(
        *,
        run: SurveyRun,
        question: Question,
        option: AnswerOption,
    ) -> UserAnswer:
        if option.question_id != question.id:
            raise ValidationError({"option_id": "Вариант не принадлежит вопросу"})
        if question.survey_id != run.survey_id:
            raise ValidationError({"question_id": "Вопрос не принадлежит опросу"})
        if run.answers.filter(question=question).exists():
            raise ValidationError({"question_id": "Вопрос уже отвечён"})

        return UserAnswer.objects.create(
            run=run,
            question=question,
            selected_option=option,
        )
