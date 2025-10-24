from django.contrib import admin
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.urls import include, path


def healthz(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz", healthz, name="healthz"),
    path("api/v1/", include("src.config.urls_api_v1")),
]
