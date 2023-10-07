from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Переопределение модели пользователя."""

    id = models.AutoField(primary_key=True)

    username = models.CharField('Имя пользователя',
                                db_index=True,
                                max_length=150,
                                unique=True)

    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=254,
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )

    password = models.CharField(
        'Пароль',
        max_length=100,
    )

    REQUIRED_FIELDS = ('email',)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
