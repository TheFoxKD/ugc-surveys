from django.contrib import admin

from .models import Identity, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "is_active", "is_staff", "last_login")
    search_fields = ("username",)


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "provider", "value", "created_at")
    list_filter = ("provider",)
    search_fields = ("value",)
