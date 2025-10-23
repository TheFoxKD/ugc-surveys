from typing import ClassVar

from django.db import models

from src.common.models import TimeStampedModel
from src.users.enums import IdentityProvider


class Identity(TimeStampedModel):
    """Связь пользователя с внешней идентичностью.

    Сейчас поддерживаем только provider='email'. В будущем можно добавить другие.
    (provider, value) уникальны глобально.
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="identities",
    )
    provider = models.CharField(max_length=32, choices=IdentityProvider.choices)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = "user_identities"
        verbose_name = "Identity"
        verbose_name_plural = "Identities"
        constraints: ClassVar[list[models.UniqueConstraint]] = [
            models.UniqueConstraint(
                fields=["provider", "value"],
                name="identity_provider_value_unique",
            ),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.provider}:{self.value}"
