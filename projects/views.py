from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import ProjectForm
from users.models import Profile
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Project


def project_list(request):
    projects = Project.objects.all().order_by("-created_at")

    paginator = Paginator(projects, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects,
            "page_obj": page_obj,
            "query_prefix": "",
        },
    )

@login_required(login_url="/users/login/")
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            profile = request.user.profile

            project = form.save(commit=False)
            project.owner = profile
            project.save()

            project.participants.add(profile)

            return redirect("/")

    else:
        form = ProjectForm()

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form
        }
    )

def edit_project(request, pk):

    project = Project.objects.get(id=pk)

    if request.user.profile != project.owner:
        return redirect("/")

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            instance=project
        )

        if form.is_valid():
            form.save()

            return redirect(
                f"/projects/{project.id}/"
            )

    else:

        form = ProjectForm(
            instance=project
        )

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
        }
    )

def project_detail(request, pk):
    project = Project.objects.get(id=pk)

    return render(
        request,
        "projects/project-details.html",
        {
            "project": project,
        }
    )

@require_POST
def complete_project(request, pk):

    project = Project.objects.get(id=pk)

    if request.user.profile != project.owner:
        return JsonResponse(
            {"status": "error"}
        )

    project.status = "closed"
    project.save()

    return JsonResponse(
        {"status": "ok"}
    )


@require_POST
def toggle_participate(request, pk):

    project = Project.objects.get(id=pk)

    profile = request.user.profile

    if project.status == "closed":
        return JsonResponse(
            {
                "status": "error",
                "message": "Проект закрыт"
            }
        )

    if profile in project.participants.all():

        if profile == project.owner:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Автор проекта не может покинуть проект"
                }
            )

        project.participants.remove(profile)

        return JsonResponse(
            {
                "status": "ok",
                "participant": False,
            }
        )

    project.participants.add(profile)

    return JsonResponse(
        {
            "status": "ok",
            "participant": True,
        }
    )
