from django.urls import path

from src.surveys.views import AnswerSubmitView, NextQuestionView

app_name = "runs"

urlpatterns = [
    path("next-question", NextQuestionView.as_view(), name="next-question"),
    path("answer", AnswerSubmitView.as_view(), name="answer-submit"),
]
