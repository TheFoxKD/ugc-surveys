import logging

from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    EmailTokenObtainPairSerializer,
    LogoutSerializer,
    RegisterSerializer,
)

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request=RegisterSerializer,
        responses={status.HTTP_201_CREATED: RegisterSerializer},
        summary="Регистрация пользователя",
        description="Создаёт пользователя с email и паролем.",
        examples=[
            OpenApiExample(
                "Successful response",
                description="Пример успешного ответа",
                value={
                    "id": 1,
                    "email": "krishtopadenis@gmail.com",
                    "username": "f65eb017-cf9e-44a4-90ee-a37f3a6c9386",
                },
                response_only=True,
            ),
            OpenApiExample(
                "Credentials",
                description="Пример запроса",
                value={
                    "email": "krishtopadenis@gmail.com",
                    "password": "S3cur3Passw0rd",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = serializer.save()
        return Response(
            serializer.to_representation(created),
            status=status.HTTP_201_CREATED,
        )


class TokenObtainView(APIView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request=EmailTokenObtainPairSerializer,
        responses={status.HTTP_200_OK: EmailTokenObtainPairSerializer},
        summary="Получение JWT",
        description="Возвращает пару access/refresh по email и паролю.",
        examples=[
            OpenApiExample(
                "JWT token pair",
                description="Пример успешного ответа",
                value={
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                },
                response_only=True,
            ),
            OpenApiExample(
                "Credentials",
                description="Пример запроса",
                value={
                    "email": "krishtopadenis@gmail.com",
                    "password": "S3cur3Passw0rd",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request: Request) -> Response:
        serializer = EmailTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request=TokenRefreshSerializer,
        responses={status.HTTP_200_OK: TokenRefreshSerializer},
        summary="Обновление access-токена",
        description="Принимает refresh и возвращает новый access-токен.",
        examples=[
            OpenApiExample(
                "Refresh token request",
                description="Пример запроса",
                value={
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh-token",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Access token response",
                description="Пример успешного ответа",
                value={
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.new-access-token",
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request: Request) -> Response:
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        request=LogoutSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        summary="Выход пользователя",
        description="Принимает refresh-токен и помещает его в blacklist.",
        examples=[
            OpenApiExample(
                "Logout request",
                description="Пример запроса",
                value={
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh-token",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request: Request) -> Response:
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
