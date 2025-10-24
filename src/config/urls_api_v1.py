from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

app_name = "api_v1"
urlpatterns = [
    path("schema", SpectacularAPIView.as_view(), name="schema"),
    path("docs", SpectacularSwaggerView.as_view(url_name="api_v1:schema"), name="docs"),
    path("auth/", include("src.users.urls")),
    path("surveys/", include("src.surveys.urls")),
]
