import json

from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, RegisterForm, UserForm
from .models import Skill, User


USERS_PER_PAGE = 12
DEFAULT_PAGE_NUMBER = 1
SKILLS_SUGGESTIONS_LIMIT = 10


def users_list(request):
    active_skill = request.GET.get("skill")

    users = (
        User.objects
        .prefetch_related("skills")
        .order_by("-created_at")
    )

    if active_skill:
        users = users.filter(skills__name=active_skill)

    paginator = Paginator(users, USERS_PER_PAGE)
    page_number = request.GET.get("page", DEFAULT_PAGE_NUMBER)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "users/participants.html",
        {
            "page_obj": page_obj,
            "all_skills": Skill.objects.all(),
            "active_skill": active_skill,
            "query_prefix": "",
        },
    )


def user_detail(request, pk):
    user = get_object_or_404(
        User.objects.prefetch_related(
            "skills",
            "owned_projects",
            "owned_projects__participants",
        ),
        id=pk,
    )

    return render(
        request,
        "users/user-details.html",
        {
            "user": user,
        },
    )


def edit_profile(request):
    form = UserForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f"/users/{request.user.id}/")

    return render(
        request,
        "users/edit_profile.html",
        {
            "user": request.user,
            "form": form,
        },
    )


def change_password(request):
    form = PasswordChangeForm(
        request.user,
        request.POST or None,
    )

    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)

        return redirect(f"/users/{request.user.id}/")

    return render(
        request,
        "users/change_password.html",
        {
            "form": form,
        },
    )


def logout_view(request):
    logout(request)
    return redirect("/")


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user:
            login(request, user)
            return redirect("/")

        form.add_error(None, "Неверный email или пароль")

    return render(
        request,
        "users/login.html",
        {
            "form": form,
        },
    )


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]

        user = User.objects.create_user(
            email=email,
            password=form.cleaned_data["password"],
            name=form.cleaned_data["name"],
            surname=form.cleaned_data["surname"],
        )

        login(request, user)
        return redirect("/")

    return render(
        request,
        "users/register.html",
        {
            "form": form,
        },
    )


def skills_list(request):
    query = request.GET.get("q", "")

    skills = Skill.objects.filter(
        name__icontains=query,
    )[:SKILLS_SUGGESTIONS_LIMIT]

    return JsonResponse(
        [
            {
                "id": skill.id,
                "name": skill.name,
            }
            for skill in skills
        ],
        safe=False,
    )


def add_skill(request, user_id):
    user = get_object_or_404(User, id=user_id)

    data = json.loads(request.body)

    if "skill_id" in data:
        skill = get_object_or_404(Skill, id=data["skill_id"])
    else:
        skill, _ = Skill.objects.get_or_create(
            name=data["name"],
        )

    user.skills.add(skill)

    return JsonResponse(
        {
            "id": skill.id,
            "name": skill.name,
        }
    )


def remove_skill(request, user_id, skill_id):
    user = get_object_or_404(User, id=user_id)
    skill = get_object_or_404(Skill, id=skill_id)

    user.skills.remove(skill)

    return JsonResponse(
        {
            "status": "ok",
        }
    )
