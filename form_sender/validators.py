"""Валидаторы для API приложения forms.

Содержит представления для следующих форм:
- validate_phone_number: валидатор правильности введенного номера телефона.
"""

import re
from rest_framework import serializers

def validate_phone_number(value):
    """Валидация номера телефона."""
    clean_numder = re.sub(r'[\s\-()]', '', value)
    pattern = r'^\+7\d{10}$$'
    if not re.match(pattern, clean_numder):
        raise serializers.ValidationError(
            'Номер телефона должен быть в формате +79998887766 или 89998887766'
        )
    return value

def validate_name_characters(value):
    """Валидация имени."""
    pattern = r'^[a-zA-Zа-яА-я]+$'
    if not re.match(pattern, value):
        raise serializers.ValidationError(
            'Имя должно состоять из букв'
        )
    return value