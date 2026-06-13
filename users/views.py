from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .forms import (
    LoginForm,
    RegisterForm,
    ProfileForm,
)

from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from .models import Profile, Skill


def users_list(request):

    active_skill = request.GET.get("skill")

    profiles = Profile.objects.all()

    if active_skill:
        profiles = profiles.filter(
            skills__name=active_skill
        )

    paginator = Paginator(profiles, 12)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "users/participants.html",
        {
            "page_obj": page_obj,
            "all_skills": Skill.objects.all().order_by("name"),
            "active_skill": active_skill,
            "query_prefix": "",
        }
    )

def user_detail(request, pk):
    profile = Profile.objects.get(id=pk)

    return render(
        request,
        "users/user-details.html",
        {
            "user": profile,
        }
    )


def edit_profile(request):

    profile = request.user.profile

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()

            return redirect(
                f"/users/{profile.id}/"
            )

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "users/edit_profile.html",
        {
            "user": profile,
            "form": form,
        }
    )

def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            return redirect(
                f"/users/{request.user.profile.id}/"
            )

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "users/change_password.html",
        {
            "form": form,
        }
    )

def logout_view(request):
    logout(request)
    return redirect("/")

def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:
                login(request, user)
                return redirect("/")
            else:
                form.add_error(
                    None,
                    "Неверный email или пароль"
                )

    else:
        form = LoginForm()

    return render(
        request,
        "users/login.html",
        {
            "form": form,
        }
    )

def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            if User.objects.filter(username=email).exists():
                form.add_error("email", "Пользователь уже существует")

            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=form.cleaned_data["password"]
                )

                Profile.objects.create(
                    user=user,
                    name=form.cleaned_data["name"],
                    surname=form.cleaned_data["surname"]
                )

                login(request, user)
                return redirect("/")

    else:
        form = RegisterForm()

    return render(
        request,
        "users/register.html",
        {
            "form": form,
        }
    )

def skills_list(request):

    q = request.GET.get("q", "")

    skills = Skill.objects.filter(
        name__icontains=q
    ).order_by("name")[:10]

    return JsonResponse(
        [
            {
                "id": skill.id,
                "name": skill.name,
            }
            for skill in skills
        ],
        safe=False
    )


def add_skill(request, user_id):

    profile = Profile.objects.get(id=user_id)

    data = json.loads(request.body)

    if "skill_id" in data:

        skill = Skill.objects.get(
            id=data["skill_id"]
        )

    else:

        skill, _ = Skill.objects.get_or_create(
            name=data["name"]
        )

    profile.skills.add(skill)

    return JsonResponse(
        {
            "id": skill.id,
            "name": skill.name,
        }
    )


def remove_skill(request, user_id, skill_id):

    profile = Profile.objects.get(id=user_id)

    skill = Skill.objects.get(id=skill_id)

    profile.skills.remove(skill)

    return JsonResponse(
        {
            "status": "ok"
        }
    )
