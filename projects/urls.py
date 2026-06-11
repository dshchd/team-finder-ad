from django.urls import path

from .views import (
    project_list,
    create_project,
    project_detail,
)

app_name = "projects"

urlpatterns = [
    path("", project_list, name="project_list"),

    path(
        "projects/list/",
        project_list,
        name="project_list_page"
    ),

    path(
        "projects/create-project/",
        create_project,
        name="create_project"
    ),

    path(
        "projects/<int:pk>/",
        project_detail,
        name="project_detail"
    ),
]
