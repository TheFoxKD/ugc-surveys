from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from src.surveys.models import Survey


class IsSurveyAuthor(BasePermission):
    """Разрешение: текущий пользователь является автором опроса."""

    def has_object_permission(
        self,
        request: Request,
        _view: APIView,
        obj: Survey,
    ) -> bool:
        return obj.author_id == request.user.id

    def has_permission(self, request: Request, _view: APIView) -> bool:
        return request.user and request.user.is_authenticated
