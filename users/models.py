from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Навык'
    )

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    name = models.CharField(
        'Имя',
        max_length=100,
        blank=True
    )
    
    surname = models.CharField(
        'Фамилия',
        max_length=100,
        blank=True
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    about = models.TextField(
        'О себе',
        blank=True
    )

    phone = models.CharField(
        'Телефон',
        max_length=20,
        blank=True
    )

    github_url = models.URLField(
    'GitHub',
    blank=True
    )

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='profiles'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username
