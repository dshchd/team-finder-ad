from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import ProjectForm
from users.models import Profile

from .models import Project


def project_list(request):
    projects = Project.objects.all().order_by("-created_at")

    paginator = Paginator(projects, 6)
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

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            profile = Profile.objects.first()

            project = form.save(commit=False)
            project.owner = profile
            project.save()

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

def project_detail(request, pk):
    project = Project.objects.get(id=pk)

    return render(
        request,
        "projects/project-details.html",
        {
            "project": project,
            "user": project.owner,
        }
    )
