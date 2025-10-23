from django.urls import path

from .views import LogoutView, RegisterView, TokenObtainView, TokenRefreshView

urlpatterns = [
    path("register", RegisterView.as_view(), name="auth-register"),
    path("token", TokenObtainView.as_view(), name="auth-token"),
    path("token/refresh", TokenRefreshView.as_view(), name="auth-token-refresh"),
    path("logout", LogoutView.as_view(), name="auth-logout"),
]
