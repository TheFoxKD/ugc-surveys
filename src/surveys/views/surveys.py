from typing import Any

from django.db.models import ProtectedError, QuerySet
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from src.surveys.models import Survey
from src.surveys.permissions import IsSurveyAuthor
from src.surveys.serializers import (
    SurveyCreateUpdateSerializer,
    SurveyDetailSerializer,
    SurveySerializer,
)
from src.surveys.services import SurveyStatsService


class SurveyListView(generics.ListAPIView):
    queryset = Survey.objects.select_related("author").all()
    serializer_class = SurveySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        summary="Список опросов текущего автора",
        responses=SurveySerializer(many=True),
        examples=[
            OpenApiExample(
                "List surveys",
                value=[
                    {
                        "id": 1,
                        "title": "Овощи",
                        "created_at": "2025-10-20T10:00:00Z",
                        "updated_at": "2025-10-21T10:00:00Z",
                    },
                ],
                response_only=True,
            ),
        ],
    )
    def get_queryset(self) -> QuerySet[Survey]:
        return self.queryset.filter(author=self.request.user)


class SurveyCreateView(generics.CreateAPIView):
    queryset = Survey.objects.select_related("author").all()
    serializer_class = SurveyCreateUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        summary="Создание опроса",
        request=SurveyCreateUpdateSerializer,
        responses={status.HTTP_201_CREATED: SurveySerializer},
        examples=[
            OpenApiExample(
                "Create survey",
                request_only=True,
                value={"title": "Любишь ли ты помидоры?"},
            ),
        ],
    )
    def get_serializer_context(self) -> dict[str, Any]:
        context = super().get_serializer_context()
        context["author"] = self.request.user
        return context

    def create(
        self,
        request: Request,
        *_args: object,
        **_kwargs: object,
    ) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        survey = serializer.save()
        return Response(
            SurveySerializer(survey).data,
            status=status.HTTP_201_CREATED,
        )


class SurveyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.select_related("author").prefetch_related(
        "questions__answer_options",
    )
    serializer_class = SurveyDetailSerializer
    permission_classes = (IsSurveyAuthor,)

    def get_queryset(self) -> QuerySet[Survey]:
        return self.queryset.filter(author=self.request.user)

    @extend_schema(summary="Подробности опроса")
    def get(
        self,
        request: Request,
        *args: object,
        **kwargs: object,
    ) -> Response:
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление опроса",
        request=SurveyCreateUpdateSerializer,
        responses=SurveyDetailSerializer,
    )
    def patch(
        self,
        request: Request,
        *_args: object,
        **_kwargs: object,
    ) -> Response:
        survey = self.get_object()
        serializer = SurveyCreateUpdateSerializer(
            instance=survey,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        survey = serializer.save()
        return Response(SurveyDetailSerializer(survey).data)

    @extend_schema(summary="Удаление опроса")
    def delete(
        self,
        _request: Request,
        *_args: object,
        **_kwargs: object,
    ) -> Response:
        survey = self.get_object()
        try:
            survey.delete()
        except ProtectedError as exc:
            msg = "Нельзя удалить опрос с ответами"
            raise ValidationError(msg) from exc
        return Response(status=status.HTTP_204_NO_CONTENT)


class SurveyStatsView(generics.RetrieveAPIView):
    queryset = Survey.objects.all()
    permission_classes = (IsSurveyAuthor,)

    @extend_schema(
        summary="Статистика по опросу",
        responses={status.HTTP_200_OK: SurveyDetailSerializer},
        examples=[
            OpenApiExample(
                "Survey stats",
                value={
                    "total_runs": 10,
                    "avg_duration_seconds": 42.5,
                    "questions": [
                        {
                            "question_id": 1,
                            "text": "Любишь ли ты помидоры?",
                            "options": [
                                {"option_id": 1, "text": "Да", "answers_count": 8},
                                {"option_id": 2, "text": "Нет", "answers_count": 2},
                            ],
                            "top_option_id": 1,
                        },
                    ],
                },
                response_only=True,
            ),
        ],
    )
    def get(
        self,
        _request: Request,
        *_args: object,
        **_kwargs: object,
    ) -> Response:
        survey = self.get_object()
        stats = SurveyStatsService.collect(survey)
        return Response(stats)
