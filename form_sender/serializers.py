"""Сериализаторы для форм.

Этот модуль содержит сериализаторы, используемые для преобразования
и валидации данных форм.

Включенные сериализаторы:
- FeedbackFormSerializer: для формы обратной связи.
"""

import re

from rest_framework import serializers

from .validators import validate_phone_number, validate_name_characters


class FormatterPhoneNumber(serializers.CharField):
    """Сериализатор для форматирования номера телефона."""

    default_validators = [validate_phone_number]

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        cleaned_value = re.sub(r'[\s\-()]', '', value)
        if (
            cleaned_value
            and cleaned_value.startswith('+7')
            and len(cleaned_value) == 12
        ):
            country_code = cleaned_value[0:2]
            area_code = cleaned_value[2:5]
            part1 = cleaned_value[5:8]
            part2 = cleaned_value[8:10]
            part3 = cleaned_value[10:12]
            return f"{country_code} ({area_code}) {part1}-{part2}-{part3}"
        return cleaned_value


class FeedbackFormSerializer(serializers.Serializer):
    """Сериализатор для формы обратной связи."""

    name = serializers.CharField(
        max_length=255, validators=[validate_name_characters]
    )
    phone_number = FormatterPhoneNumber(max_length=25)
    message = serializers.CharField(max_length=1000)  # около 200 слов
