from django.urls import path

from src.surveys.views import QuestionCreateView, QuestionDeleteView, QuestionUpdateView

app_name = "questions"
urlpatterns = [
    path("create", QuestionCreateView.as_view(), name="question-create"),
    path("<int:question_id>", QuestionUpdateView.as_view(), name="question-update"),
    path(
        "<int:question_id>/delete",
        QuestionDeleteView.as_view(),
        name="question-delete",
    ),
]
