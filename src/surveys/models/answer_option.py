from typing import ClassVar

from django.db import models

from src.common.models import TimeStampedModel


class AnswerOption(TimeStampedModel):
    """Вариант ответа для вопроса."""

    question = models.ForeignKey(
        "surveys.Question",
        on_delete=models.CASCADE,
        related_name="answer_options",
    )
    text = models.CharField(max_length=255)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "survey_answer_options"
        verbose_name = "Answer option"
        verbose_name_plural = "Answer options"
        ordering = ("position",)
        constraints: ClassVar[list[models.UniqueConstraint]] = [
            models.UniqueConstraint(
                fields=["question", "position"],
                name="answer_option_unique_position_per_question",
            ),
        ]

    def __str__(self) -> str:
        return self.text
