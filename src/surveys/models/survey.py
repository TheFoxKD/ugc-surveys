from typing import ClassVar

from django.db import models

from src.common.models import TimeStampedModel


class Survey(TimeStampedModel):
    """Опрос создаётся автором и содержит вопросы."""

    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="surveys",
    )

    class Meta:
        db_table = "surveys"
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["author"], name="idx_survey_author"),
        ]

    def __str__(self) -> str:
        return self.title
