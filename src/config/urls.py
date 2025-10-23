from django.contrib import admin
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def healthz(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    # Health
    path("healthz", healthz, name="healthz"),
    # API schema & docs (authorized)
    path("api/v1/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Auth
    path("api/v1/auth/", include("src.users.urls")),
]
