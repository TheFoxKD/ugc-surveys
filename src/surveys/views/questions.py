from django.db.models import ProtectedError
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from src.surveys.models import Question, Survey
from src.surveys.permissions import IsSurveyAuthor
from src.surveys.serializers import (
    QuestionCreateUpdateSerializer,
    QuestionNestedSerializer,
)


class BaseSurveyQuestionView(generics.GenericAPIView):
    permission_classes = (IsSurveyAuthor,)

    def get_survey(self) -> Survey:
        return generics.get_object_or_404(
            Survey,
            pk=self.kwargs["pk"],
            author=self.request.user,
        )


class QuestionCreateView(BaseSurveyQuestionView):
    serializer_class = QuestionCreateUpdateSerializer

    @extend_schema(
        summary="Добавить вопрос",
        request=QuestionCreateUpdateSerializer,
        responses={status.HTTP_201_CREATED: QuestionNestedSerializer},
        examples=[
            OpenApiExample(
                "Create question",
                value={"text": "Любишь ли ты огурцы?", "position": 2},
                request_only=True,
            ),
        ],
    )
    def post(
        self,
        request: Request,
        *_args: object,
        **_kwargs: object,
    ) -> Response:
        survey = self.get_survey()
        serializer = self.get_serializer(data=request.data, context={"survey": survey})
        serializer.is_valid(raise_exception=True)
        question = serializer.save()
        return Response(
            QuestionNestedSerializer(question).data,
            status=status.HTTP_201_CREATED,
        )


class QuestionUpdateView(BaseSurveyQuestionView):
    serializer_class = QuestionCreateUpdateSerializer

    def get_object(self) -> Question:
        survey = self.get_survey()
        return generics.get_object_or_404(
            Question,
            pk=self.kwargs["question_id"],
            survey=survey,
        )

    @extend_schema(
        summary="Обновить вопрос",
        request=QuestionCreateUpdateSerializer,
        responses=QuestionNestedSerializer,
    )
    def patch(
        self,
        request: Request,
        *_args: object,
        **_kwargs: object,
    ) -> Response:
        question = self.get_object()
        serializer = self.get_serializer(
            instance=question,
            data=request.data,
            partial=True,
            context={"survey": question.survey},
        )
        serializer.is_valid(raise_exception=True)
        question = serializer.save()
        return Response(QuestionNestedSerializer(question).data)


class QuestionDeleteView(BaseSurveyQuestionView):
    @extend_schema(summary="Удалить вопрос")
    def delete(
        self,
        _request: Request,
        *_args: object,
        **_kwargs: object,
    ) -> Response:
        question = self.get_object()
        try:
            question.delete()
        except ProtectedError as exc:
            msg = "Нельзя удалить вопрос с ответами"
            raise ValidationError(msg) from exc
        return Response(status=status.HTTP_204_NO_CONTENT)
