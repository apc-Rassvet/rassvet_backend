"""Модуль с моделями пользователей для проекта 'АПЦ Рассвет'.

Этот модуль содержит модели, связанные с пользователями в проекте.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class RassvetUser(AbstractUser):
    """Пользовательская модель для проекта 'Рассвет'.

    Эта модель расширяет стандартную модель пользователя Django (AbstractUser),
    делая email обязательным и уникальным полем. Модель используется как
    основная модель пользователя для проекта и настроена через параметр
    AUTH_USER_MODEL в настройках проекта.
    """

    email = models.EmailField('email address', unique=True, blank=False)
    REQUIRED_FIELDS = ['email']
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'
