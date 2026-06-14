from django.conf import settings
from django.db import models


PROJECT_NAME_MAX_LENGTH = 200
PROJECT_STATUS_MAX_LENGTH = 10


class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Открытый"
        CLOSED = "closed", "Закрытый"

    name = models.CharField(
        "Название",
        max_length=PROJECT_NAME_MAX_LENGTH,
    )
    description = models.TextField(
        "Описание",
        blank=True,
    )
    github_url = models.URLField(
        "GitHub проекта",
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="projects",
    )
    status = models.CharField(
        "Статус",
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=Status.choices,
        default=Status.OPEN,
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name
