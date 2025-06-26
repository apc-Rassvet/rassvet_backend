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
        """Преобразует входящий номер телефона в стандартный формат.

        Принимает номер в различных форматах и возвращает его в виде:
        +7 (XXX) XXX-XX-XX для российских номеров.

        Примеры КОРРЕКТНЫХ входных форматов:
        - "+79161234567"
        - "+7 916 123 45 67"
        - "+7-916-123-45-67"
        - "+7(916)123-45-67"
        """
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
            return f'{country_code} ({area_code}) {part1}-{part2}-{part3}'
        return cleaned_value


class FeedbackFormSerializer(serializers.Serializer):
    """Сериализатор для формы обратной связи."""

    name = serializers.CharField(
        max_length=255, validators=[validate_name_characters]
    )
    phone_number = FormatterPhoneNumber(
        max_length=25,
        help_text=(
            'Российский номер телефона в международном формате. '
            'Автоматически форматируется в +7 (XXX) XXX-XX-XX. '
            'Примеры корректных форматов: +79161234567, +7 916 123 45 67, '
            '+7-916-123-45-67, +7(916)123-45-67'
        ),
    )
    message = serializers.CharField(max_length=1000)
    accept_terms = serializers.BooleanField(
        required=True,
        help_text='Согласие на обработку персональных данных (обязательно)',
    )

    def validate_accept_terms(self, value):
        """Проверяет, что пользователь принял условия."""
        if not value:
            raise serializers.ValidationError(
                'Необходимо принять условия обработки персональных данных'
            )
        return value


class FeedbackSuccessResponseSerializer(serializers.Serializer):
    """Сериализатор для успешного ответа формы обратной связи."""

    status = serializers.CharField()
    message = serializers.CharField()


class FeedbackErrorResponseSerializer(serializers.Serializer):
    """Сериализатор для ошибок валидации формы обратной связи."""

    name = serializers.ListField(child=serializers.CharField(), required=False)
    phone_number = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    message = serializers.ListField(
        child=serializers.CharField(), required=False
    )


class ThrottleErrorResponseSerializer(serializers.Serializer):
    """Сериализатор для ошибки превышения лимита запросов."""

    detail = serializers.CharField()
