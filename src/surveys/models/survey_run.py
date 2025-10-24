from typing import ClassVar

from django.db import models
from django.utils import timezone

from src.common.models import TimeStampedModel


class SurveyRun(TimeStampedModel):
    """Попытка прохождения опроса пользователем."""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="survey_runs",
    )
    survey = models.ForeignKey(
        "surveys.Survey",
        on_delete=models.CASCADE,
        related_name="runs",
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "survey_runs"
        verbose_name = "Survey run"
        verbose_name_plural = "Survey runs"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["survey"], name="idx_run_survey"),
        ]
        constraints: ClassVar[list[models.UniqueConstraint]] = [
            models.UniqueConstraint(
                fields=["user", "survey"],
                condition=models.Q(finished_at__isnull=True),
                name="unique_active_run_per_user",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.pk=} {self.user.username=} {self.survey.title=}"

    @property
    def is_finished(self) -> bool:
        return self.finished_at is not None

    def mark_finished(self) -> None:
        if self.finished_at is None:
            self.finished_at = timezone.now()
            self.save(update_fields=["finished_at", "updated_at"])
