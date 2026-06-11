from django.shortcuts import render

from .models import Profile


def users_list(request):
    profiles = Profile.objects.all()

    return render(
        request,
        "users/participants.html",
        {
            "users": profiles,
            "page_obj": profiles,
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
    profile = Profile.objects.first()

    return render(
        request,
        "users/edit_profile.html",
        {
            "user": profile,
            "form": None,
        }
    )
