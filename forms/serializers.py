"""Сериализаторы для форм.

Этот модуль содержит сериализаторы, используемые для преобразования
и валидации данных форм.

Включенные сериализаторы:
- FeedbackFormSerializer: для формы обратной связи.
"""

from rest_framework import serializers
from .validators import validate_phone_number

class FeedbackFormSerializer(serializers.Serializer):
    """Сериализатор для формы обратной связи."""

    name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=25,validators=[validate_phone_number])
    message = serializers.CharField(max_length=1000) # около 200 слов