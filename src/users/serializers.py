import uuid
from dataclasses import dataclass

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

from .enums import IdentityProvider
from .models import Identity, User


@dataclass
class CreatedUser:
    user: User
    identity: Identity


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_email(self, value: str) -> str:
        if Identity.objects.filter(
            provider=IdentityProvider.EMAIL,
            value=value,
        ).exists():
            msg = "Пользователь с таким email уже существует"
            raise serializers.ValidationError(msg)
        return value

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data: dict[str, object]) -> CreatedUser:
        email: str = validated_data["email"]
        password: str = validated_data["password"]

        # Генерируем технический username (чтобы не требовать его от клиента)
        username = str(uuid.uuid4())

        user = User.objects.create_user(username=username, password=password)
        identity = Identity.objects.create(
            user=user,
            provider=IdentityProvider.EMAIL,
            value=email,
        )
        return CreatedUser(user=user, identity=identity)

    def to_representation(self, instance: CreatedUser) -> dict[str, object]:
        return {
            "id": instance.user.pk,
            "email": instance.identity.value,
            "username": instance.user.username,
        }


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Принимаем email вместо username
    username_field = "email"

    def validate(self, attrs: dict[str, object]) -> dict[str, object]:
        email = attrs.get("email")
        password = attrs.get("password")
        if not isinstance(email, str) or not isinstance(password, str):
            msg = "Неверные учетные данные"
            raise serializers.ValidationError(msg)

        try:
            identity = Identity.objects.select_related("user").get(
                provider=IdentityProvider.EMAIL,
                value=email,
            )
        except Identity.DoesNotExist as exc:
            msg = "Неверные учетные данные"
            raise serializers.ValidationError(msg) from exc

        user = identity.user
        if not user.check_password(password):
            msg = "Неверные учетные данные"
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = "Пользователь деактивирован"
            raise serializers.ValidationError(msg)

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    """Сериализатор для выхода пользователя: принимает refresh-токен."""

    refresh = serializers.CharField()

    def validate_refresh(self, value: str) -> str:
        if not value:
            msg = "refresh token required"
            raise serializers.ValidationError(msg)
        return value
