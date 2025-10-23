from django.db.models import TextChoices


class IdentityProvider(TextChoices):
    EMAIL = "email", "email"
