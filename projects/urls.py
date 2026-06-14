from django.urls import path

from .views import (complete_project, create_project, edit_project,
                    project_detail, project_list, toggle_participate)

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
        "projects/<int:pk>/edit/",
        edit_project,
        name="edit_project"
    ),

    path(
        "projects/<int:pk>/",
        project_detail,
        name="project_detail"
    ),

    path(
        "projects/<int:pk>/complete/",
        complete_project,
        name="complete_project"
    ),

    path(
        "projects/<int:pk>/toggle-participate/",
        toggle_participate,
        name="toggle_participate"
    ),
]
