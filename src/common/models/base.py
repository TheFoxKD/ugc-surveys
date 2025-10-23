from typing import ClassVar

from django.db import models


class TimeStampedModel(models.Model):
    """Базовая абстракция с временными метками.

    Всегда добавляет поля created_at и updated_at.
    Делает порядок по убыванию created_at по умолчанию.
    Создаёт индекс по created_at.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["created_at"], name="idx_created_at"),
        ]
