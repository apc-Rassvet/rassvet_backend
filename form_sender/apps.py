"""Конфигурация Django приложения form_sender."""

from django.apps import AppConfig


class FormsConfig(AppConfig):
    """Конфигурация приложения для обработки форм обратной связи."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'form_sender'
