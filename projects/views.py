from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProjectForm
from .models import Project


PROJECTS_PER_PAGE = 12
DEFAULT_PAGE_NUMBER = 1


def project_list(request):
    projects = (
        Project.objects
        .select_related("owner")
        .prefetch_related("participants")
        .order_by("-created_at")
    )

    page_number = request.GET.get("page", DEFAULT_PAGE_NUMBER)
    paginator = Paginator(projects, PROJECTS_PER_PAGE)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "projects/project_list.html",
        {
            "page_obj": page_obj,
            "query_prefix": "",
        },
    )


@login_required(login_url="/users/login/")
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)

        return redirect(f"/projects/{project.id}/")

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
        },
    )


@login_required(login_url="/users/login/")
def edit_project(request, pk):
    project = get_object_or_404(Project, id=pk)

    if request.user != project.owner:
        return redirect("/")

    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f"/projects/{project.id}/")

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
        },
    )


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects
        .select_related("owner")
        .prefetch_related("participants"),
        id=pk,
    )

    return render(
        request,
        "projects/project-details.html",
        {
            "project": project,
        },
    )


@require_POST
@login_required(login_url="/users/login/")
def complete_project(request, pk):
    project = get_object_or_404(Project, id=pk)

    if request.user != project.owner:
        return JsonResponse({"status": "error"})

    project.status = Project.Status.CLOSED
    project.save(update_fields=["status"])

    return JsonResponse({"status": "ok"})


@require_POST
@login_required(login_url="/users/login/")
def toggle_participate(request, pk):
    project = get_object_or_404(
        Project.objects.prefetch_related("participants"),
        id=pk,
    )

    if project.status == Project.Status.CLOSED:
        return JsonResponse(
            {
                "status": "error",
                "message": "Проект закрыт",
            }
        )

    if project.participants.filter(id=request.user.id).exists():
        if request.user == project.owner:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Автор проекта не может покинуть проект",
                }
            )

        project.participants.remove(request.user)

        return JsonResponse(
            {
                "status": "ok",
                "participant": False,
            }
        )

    project.participants.add(request.user)

    return JsonResponse(
        {
            "status": "ok",
            "participant": True,
        }
    )
