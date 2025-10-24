from django.urls import path

from src.surveys.views import (
    AnswerOptionCreateView,
    AnswerOptionDeleteView,
    AnswerOptionUpdateView,
)

app_name = "answer-options"
urlpatterns = [
    path("create", AnswerOptionCreateView.as_view(), name="answer-option-create"),
    path(
        "<int:option_id>",
        AnswerOptionUpdateView.as_view(),
        name="answer-option-update",
    ),
    path(
        "<int:option_id>/delete",
        AnswerOptionDeleteView.as_view(),
        name="answer-option-delete",
    ),
]
