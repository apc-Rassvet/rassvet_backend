"""Представления для API приложения forms.

Содержит представления для следующих форм:
- FeedbackFormView: форма обратной связи.
"""

import os

from django.conf import settings
from django.core.mail import send_mail

from drf_spectacular.utils import (
    extend_schema,
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .openapi import feedback_form_schema
from .serializers import (
    FeedbackFormSerializer,
)


@extend_schema(tags=['Forms group'])
@feedback_form_schema
class FeedbackFormView(APIView):
    """Форма обратной связи."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'feedback'

    def post(self, request, *args, **kwargs):
        """Создание новой записи в базе данных."""
        serializer = FeedbackFormSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            phone_number = serializer.validated_data['phone_number']
            message = serializer.validated_data['message']
            send_mail(
                'Форма обратной связи',
                f'{name} оставил заявку на обратную связь.'
                f'Телефон: {phone_number}. Сообщение: {message}',
                settings.EMAIL_HOST_USER,
                [os.environ.get('EMAIL_SEND')],
                fail_silently=not settings.DEBUG,
            )
            return Response(
                {
                    'status': 'success',
                    'message': 'Сообщение отправлено успешно!',
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
