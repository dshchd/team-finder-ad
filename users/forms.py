from django import forms
from .models import Profile


class LoginForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )

class RegisterForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=100)

    surname = forms.CharField(label="Фамилия", max_length=100)

    email = forms.EmailField(label="Email")

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "avatar",
            "name",
            "surname",
            "about",
            "phone",
            "github_url",
        ]
