from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response

from src.surveys.models import AnswerOption, Question, Survey
from src.surveys.serializers import (
    AnswerResultSerializer,
    AnswerSubmitSerializer,
    NextQuestionSerializer,
)
from src.surveys.services import SurveyRunService


class NextQuestionView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        summary="Следующий вопрос",
        responses={status.HTTP_200_OK: NextQuestionSerializer},
        examples=[
            OpenApiExample(
                "Next question",
                value={
                    "run_id": 5,
                    "question": {
                        "id": 42,
                        "text": "Любишь ли ты помидоры?",
                        "position": 1,
                        "answer_options": [
                            {"id": 101, "text": "Да", "position": 1},
                            {"id": 102, "text": "Нет", "position": 2},
                        ],
                    },
                },
                response_only=True,
            ),
        ],
    )
    def get(self, request: Request, pk: int) -> Response:
        survey = get_object_or_404(Survey, pk=pk)
        run = SurveyRunService.get_or_create_active_run(
            survey=survey,
            user=request.user,
        )
        question = SurveyRunService.next_question(run)
        if question is None:
            run.mark_finished()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = NextQuestionSerializer({"run_id": run.pk, "question": question}).data
        return Response(data)


class AnswerSubmitView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AnswerSubmitSerializer

    @extend_schema(
        summary="Отправить ответ",
        request=AnswerSubmitSerializer,
        responses={status.HTTP_200_OK: AnswerResultSerializer},
        examples=[
            OpenApiExample(
                "Submit answer",
                value={"question_id": 42, "option_id": 101},
                request_only=True,
            ),
            OpenApiExample(
                "Next question available",
                value={
                    "run_id": 5,
                    "completed": False,
                    "question": {
                        "id": 43,
                        "text": "Следующий вопрос?",
                        "position": 2,
                        "answer_options": [
                            {"id": 111, "text": "Да", "position": 1},
                            {"id": 112, "text": "Нет", "position": 2},
                        ],
                    },
                },
                response_only=True,
            ),
            OpenApiExample(
                "Survey completed",
                value={"run_id": 5, "completed": True, "question": None},
                response_only=True,
            ),
        ],
    )
    def post(self, request: Request, pk: int) -> Response:
        survey = get_object_or_404(Survey, pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        run = SurveyRunService.get_or_create_active_run(
            survey=survey,
            user=request.user,
        )
        question = get_object_or_404(
            Question,
            pk=serializer.validated_data["question_id"],
            survey=survey,
        )
        option = get_object_or_404(
            AnswerOption,
            pk=serializer.validated_data["option_id"],
            question=question,
        )

        SurveyRunService.create_answer(run=run, question=question, option=option)

        next_q = SurveyRunService.next_question(run)
        completed = next_q is None
        if completed:
            run.mark_finished()

        payload = {"run_id": run.pk, "completed": completed, "question": next_q}
        data = AnswerResultSerializer(payload).data
        return Response(data, status=status.HTTP_200_OK)
