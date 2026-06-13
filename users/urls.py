from django.urls import path

from .views import (
    users_list,
    user_detail,
    edit_profile,
    change_password,
    logout_view,
    login_view,
    register_view,
    skills_list,
    add_skill,
    remove_skill,
)

app_name = "users"

urlpatterns = [
    path("list/", users_list, name="users_list"),

    path(
        "edit-profile/",
        edit_profile,
        name="edit_profile"
    ),

    path(
        "change-password/",
        change_password,
        name="change_password"
    ),

    path(
        "logout/",
        logout_view,
        name="logout"
    ),

    path(
        "login/",
        login_view,
        name="login"
    ),

    path(
        "register/",
        register_view,
        name="register"
    ),

    path(
        "skills/",
        skills_list,
        name="skills_list"
    ),
    
    path(
        "<int:user_id>/skills/add/",
        add_skill,
        name="add_skill"
    ),
    
    path(
        "<int:user_id>/skills/<int:skill_id>/remove/",
        remove_skill,
        name="remove_skill"
    ),

    path(
        "<int:pk>/",
        user_detail,
        name="user_detail"
    ),
]
