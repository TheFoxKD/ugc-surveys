from typing import ClassVar

from django.db import models

from src.common.models import TimeStampedModel


class UserAnswer(TimeStampedModel):
    """Ответ пользователя в рамках прогона."""

    run = models.ForeignKey(
        "surveys.SurveyRun",
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey(
        "surveys.Question",
        on_delete=models.PROTECT,
        related_name="answers",
    )
    selected_option = models.ForeignKey(
        "surveys.AnswerOption",
        on_delete=models.PROTECT,
        related_name="selected_answers",
    )

    class Meta:
        db_table = "survey_answers"
        verbose_name = "User answer"
        verbose_name_plural = "User answers"
        constraints: ClassVar[list[models.UniqueConstraint]] = [
            models.UniqueConstraint(
                fields=["run", "question"],
                name="unique_answer_per_question_run",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.pk=} {self.run.pk=} {self.question.pk=} {self.selected_option.pk=}"
        )
