from django.db.models import ProtectedError
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from src.surveys.models import AnswerOption, Question, Survey
from src.surveys.permissions import IsSurveyAuthor
from src.surveys.serializers import (
    AnswerOptionCreateUpdateSerializer,
    AnswerOptionNestedSerializer,
)


class BaseAnswerOptionView(generics.GenericAPIView):
    permission_classes = (IsSurveyAuthor,)

    def get_survey(self) -> Survey:
        return generics.get_object_or_404(
            Survey,
            pk=self.kwargs["pk"],
            author=self.request.user,
        )

    def get_question(self) -> Question:
        survey = self.get_survey()
        return generics.get_object_or_404(
            Question,
            pk=self.kwargs["question_id"],
            survey=survey,
        )


class AnswerOptionCreateView(BaseAnswerOptionView):
    serializer_class = AnswerOptionCreateUpdateSerializer

    @extend_schema(
        summary="Добавить вариант ответа",
        request=AnswerOptionCreateUpdateSerializer,
        responses={status.HTTP_201_CREATED: AnswerOptionNestedSerializer},
        examples=[
            OpenApiExample(
                "Create option",
                value={"text": "Да", "position": 1},
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
        question = self.get_question()
        serializer = self.get_serializer(
            data=request.data,
            context={"question": question},
        )
        serializer.is_valid(raise_exception=True)
        option = serializer.save()
        return Response(
            AnswerOptionNestedSerializer(option).data,
            status=status.HTTP_201_CREATED,
        )


class AnswerOptionUpdateView(BaseAnswerOptionView):
    serializer_class = AnswerOptionCreateUpdateSerializer

    def get_object(self) -> AnswerOption:
        question = self.get_question()
        return generics.get_object_or_404(
            AnswerOption,
            pk=self.kwargs["option_id"],
            question=question,
        )

    @extend_schema(
        summary="Обновить вариант",
        request=AnswerOptionCreateUpdateSerializer,
        responses=AnswerOptionNestedSerializer,
    )
    def patch(
        self,
        request: Request,
        *_args: object,
        **_kwargs: object,
    ) -> Response:
        option = self.get_object()
        serializer = self.get_serializer(
            instance=option,
            data=request.data,
            partial=True,
            context={"question": option.question},
        )
        serializer.is_valid(raise_exception=True)
        option = serializer.save()
        return Response(AnswerOptionNestedSerializer(option).data)


class AnswerOptionDeleteView(BaseAnswerOptionView):
    @extend_schema(summary="Удалить вариант ответа")
    def delete(
        self,
        _request: Request,
        *_args: object,
        **_kwargs: object,
    ) -> Response:
        option = self.get_object()
        try:
            option.delete()
        except ProtectedError as exc:
            msg = "Нельзя удалить вариант с ответами"
            raise ValidationError(msg) from exc
        return Response(status=status.HTTP_204_NO_CONTENT)
