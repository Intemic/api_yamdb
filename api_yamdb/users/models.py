from core.constants import FIELD_LENGTH
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .enums import UserRoles


class User(AbstractUser):
    """Класс пользователей"""

    username = models.CharField(
        max_length=FIELD_LENGTH['NAME'],
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[UnicodeUsernameValidator()]
    )
    email = models.EmailField(
        max_length=FIELD_LENGTH['EMAIL'],
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=FIELD_LENGTH['NAME'],
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=FIELD_LENGTH['NAME'],
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        max_length=max(len(role) for role, _ in UserRoles.choices()),
        verbose_name='роль',
        choices=UserRoles.choices(),
        default=UserRoles.user.name
    )

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ('role',)

    def __str__(self):
        return self.username[:15]

    @property
    def is_admin(self):
        return (self.role == UserRoles.admin.name
                or self.is_superuser
                or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == UserRoles.moderator.name
