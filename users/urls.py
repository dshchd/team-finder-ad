from django.urls import path

from .views import (
    users_list,
    user_detail,
    edit_profile,
)

app_name = "users"

urlpatterns = [
    path("list/", users_list, name="users_list"),
    path("<int:pk>/", user_detail, name="user_detail"),
    path("edit-profile/", edit_profile, name="edit_profile"),
]
