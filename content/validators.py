import html

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


def validate_not_empty_html(value):
    """
    Валидатор:
    - удаляет теги, раскодирует сущности (&nbsp; → пробел),
    - проверяет, что после strip() остался хотя бы текст.
    """
    text = strip_tags(value or '')
    text = html.unescape(text)
    if not text.strip():
        raise ValidationError('Поле не может быть пустым')
