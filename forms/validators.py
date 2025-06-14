"""Валидаторы для API приложения forms.

Содержит представления для следующих форм:
- validate_phone_number: валидатор правильности введенного номера телефона.
"""

import re
from rest_framework import serializers

def validate_phone_number(value):
    """Валидация номера телефона."""
    pattern = r'^((\+7|8)[ \-]?)?$?\d{3}$?[ \-]?\d{3}[ \-]?\d{2}[ \-]?\d{2}$'
    if not re.match(pattern, value):
        raise serializers.ValidationError(
            'Номер телефона должен быть в формате +79998887766 или 89998887766'
        )
    return value