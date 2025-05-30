"""Конфигурация приложения users.

Это приложение отвечает за управление пользователями.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Конфигурационный класс приложения users."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Администраторы'
