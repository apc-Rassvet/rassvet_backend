"""Модуль с валидаторами для проверки данных.

Этот модуль содержит набор функций-валидаторов, предназначенных для
проверки данных различных типов на соответствие требованиям проекта.
"""

import html

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


def validate_not_empty_html(value, error_message='Поле не может быть пустым.'):
    """Проверяет, что HTML-содержимое содержит непустой текст.

    Функция удаляет все HTML-теги, раскодирует HTML-сущности
    (например, &nbsp; преобразуется в пробел) и проверяет,
    что после очистки пробельных символов остаётся непустая строка.
    """
    text = strip_tags(value or '')
    text = html.unescape(text)
    if not text.strip():
        raise ValidationError(error_message)
