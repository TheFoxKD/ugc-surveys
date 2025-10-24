from django.urls import include, path

from src.surveys.views import (
    SurveyCreateView,
    SurveyDetailView,
    SurveyListView,
    SurveyStatsView,
)

app_name = "surveys"
urlpatterns = [
    path("list", SurveyListView.as_view(), name="survey-list"),
    path("create", SurveyCreateView.as_view(), name="survey-create"),
    path("<int:pk>", SurveyDetailView.as_view(), name="survey-detail"),
    path("<int:pk>/stats", SurveyStatsView.as_view(), name="survey-stats"),
    path(
        "<int:pk>/questions/",
        include(("src.surveys.urls.questions", "questions")),
    ),
    path(
        "<int:pk>/questions/<int:question_id>/options/",
        include(("src.surveys.urls.answer_options", "answer-options")),
    ),
    path(
        "<int:pk>/runs/",
        include(("src.surveys.urls.runs", "runs")),
    ),
]
