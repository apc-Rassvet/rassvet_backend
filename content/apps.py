"""Конфигурация приложения content.

Это приложение отвечает за управление контентом сайта.
"""

from django.apps import AppConfig


class ContentConfig(AppConfig):
    """Конфигурационный класс приложения content."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'
    verbose_name = 'Контент'

    def ready(self):
        """Запуск Django signals в приложенни."""
        import content.signals  # noqa: F401
