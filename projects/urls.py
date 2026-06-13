from django.urls import path

from .views import (
    project_list,
    create_project,
    project_detail,
    complete_project,
    toggle_participate,
    edit_project,
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
