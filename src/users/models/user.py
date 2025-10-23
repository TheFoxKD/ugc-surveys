from __future__ import annotations

from django.contrib.auth.models import AbstractUser

from src.common.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    """Custom user model.

    Username обязателен как у AbstractUser.
    Email не уникален, идентичности живут отдельно.
    """

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
