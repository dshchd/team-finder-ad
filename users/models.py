from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


SKILL_NAME_MAX_LENGTH = 100
USER_NAME_MAX_LENGTH = 100
PHONE_MAX_LENGTH = 20


class Skill(models.Model):
    name = models.CharField(
        "Навык",
        max_length=SKILL_NAME_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(
        "Email",
        unique=True,
    )
    name = models.CharField(
        "Имя",
        max_length=USER_NAME_MAX_LENGTH,
    )
    surname = models.CharField(
        "Фамилия",
        max_length=USER_NAME_MAX_LENGTH,
    )
    avatar = models.ImageField(
        "Аватар",
        upload_to="avatars/",
        blank=True,
        default="",
    )
    about = models.TextField(
        "О себе",
        blank=True,
    )
    phone = models.CharField(
        "Телефон",
        max_length=PHONE_MAX_LENGTH,
        blank=True,
    )
    github_url = models.URLField(
        "GitHub",
        blank=True,
    )
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="users",
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
        "surname",
    ]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} {self.surname}".strip() or self.email
