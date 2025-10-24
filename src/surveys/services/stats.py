from dataclasses import dataclass

from django.db.models import Avg, Count, F

from src.surveys.models import Question, Survey


@dataclass(frozen=True)
class AnswerOptionStats:
    option_id: int
    text: str
    answers_count: int


@dataclass(frozen=True)
class QuestionStats:
    question_id: int
    text: str
    options: list[AnswerOptionStats]
    top_option_id: int | None


@dataclass(frozen=True)
class SurveyStats:
    total_runs: int
    avg_duration_seconds: float | None
    questions: list[QuestionStats]


class SurveyStatsService:
    """Подготовка статистики по опросу."""

    @classmethod
    def collect(cls, survey: Survey) -> SurveyStats:
        total_runs = cls._count_runs(survey)
        avg_duration_seconds = cls._avg_duration_seconds(survey)
        questions = cls._questions_stats(survey)
        return SurveyStats(
            total_runs=total_runs,
            avg_duration_seconds=avg_duration_seconds,
            questions=questions,
        )

    @staticmethod
    def _count_runs(survey: Survey) -> int:
        return survey.runs.filter(finished_at__isnull=False).count()

    @staticmethod
    def _avg_duration_seconds(survey: Survey) -> float | None:
        result = survey.runs.filter(finished_at__isnull=False).aggregate(
            avg=Avg(F("finished_at") - F("started_at")),
        )
        delta = result["avg"]
        return float(delta.total_seconds()) if delta else None

    @classmethod
    def _questions_stats(cls, survey: Survey) -> list[QuestionStats]:
        questions = []
        for question in survey.questions.prefetch_related("answer_options"):
            options = cls._option_stats(question)
            top_option_id = cls._top_option_id(options)
            questions.append(
                QuestionStats(
                    question_id=question.id,
                    text=question.text,
                    options=options,
                    top_option_id=top_option_id,
                ),
            )
        return questions

    @staticmethod
    def _option_stats(question: Question) -> list[AnswerOptionStats]:
        option_records = (
            question.answer_options.annotate(answers_count=Count("selected_answers"))
            .values("id", "text", "answers_count")
            .order_by("position")
        )
        return [
            AnswerOptionStats(
                option_id=int(record["id"]),
                text=str(record["text"]),
                answers_count=int(record["answers_count"]),
            )
            for record in option_records
        ]

    @staticmethod
    def _top_option_id(options: list[AnswerOptionStats]) -> int | None:
        if not options:
            return None
        top = max(options, key=lambda opt: opt.answers_count)
        return top.option_id if top.answers_count > 0 else None
