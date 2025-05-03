"""Модуль конфигурации административного интерфейса для приложения users.

Этот модуль регистрирует модели приложения пользователей в административном
интерфейсе Django и настраивает отображение, фильтрацию и редактирование
пользовательских данных.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RassvetUser


@admin.register(RassvetUser)
class RassvetUserAdmin(UserAdmin):
    """Административный интерфейс для модели пользователя RassvetUser."""

    pass
