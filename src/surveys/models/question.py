from typing import ClassVar

from django.db import models

from src.common.models import TimeStampedModel


class Question(TimeStampedModel):
    """Вопрос внутри опроса."""

    survey = models.ForeignKey(
        "surveys.Survey",
        on_delete=models.CASCADE,
        related_name="questions",
    )
    text = models.TextField()
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "survey_questions"
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ("position",)
        constraints: ClassVar[list[models.UniqueConstraint]] = [
            models.UniqueConstraint(
                fields=["survey", "position"],
                name="question_unique_position_per_survey",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.position}. {self.text[:32]}"
