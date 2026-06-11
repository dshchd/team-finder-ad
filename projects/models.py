from django.db import models
from users.models import Profile


class Project(models.Model):

    STATUS_CHOICES = (
        ('open', 'Открытый'),
        ('closed', 'Закрытый'),
    )

    name = models.CharField(
    'Название',
    max_length=200
    )

    description = models.TextField(
        'Описание',
        blank=True
    )

    github_url = models.URLField(
        'GitHub проекта',
        blank=True
    )

    owner = models.ForeignKey(
    Profile,
    on_delete=models.CASCADE,
    related_name='owned_projects'
    )

    participants = models.ManyToManyField(
        Profile,
        blank=True,
        related_name='projects'
    )

    status = models.CharField(
        'Статус',
        max_length=10,
        choices=STATUS_CHOICES,
        default='open'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
