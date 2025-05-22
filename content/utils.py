"""Модуль содержит утилиты и функции, связанные с Проектом.

Функции:
    1. ckeditor_function: Функция создающая text поля для моделей проекта.
"""

from django_ckeditor_5.fields import CKEditor5Field

from .validators import validate_not_empty_html


def ckeditor_function(
    verbose_name='verbose_name',
    config_name='default',
    blank=False,
    validators=[validate_not_empty_html],
):
    """Функция создающая text поля для моделей проекта."""
    return CKEditor5Field(
        verbose_name=verbose_name,
        config_name=config_name,
        blank=blank,
        validators=validators,
    )
