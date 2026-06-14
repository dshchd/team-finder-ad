from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Skill, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "name",
        "surname",
        "phone",
        "is_staff",
    )
    search_fields = (
        "email",
        "name",
        "surname",
        "phone",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Личная информация",
            {
                "fields": (
                    "name",
                    "surname",
                    "avatar",
                    "about",
                    "phone",
                    "github_url",
                    "skills",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "surname",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
