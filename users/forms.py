from django import forms

from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )


class RegisterForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=100)
    surname = forms.CharField(label="Фамилия", max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Пользователь с таким email уже существует"
            )

        return email


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "avatar",
            "name",
            "surname",
            "about",
            "phone",
            "github_url",
        ]
