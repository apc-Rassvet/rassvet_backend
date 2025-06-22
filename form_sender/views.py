"""Представления для API приложения forms.

Содержит представления для следующих форм:
- FeedbackFormView: форма обратной связи.
"""

import os

from django.conf import settings
from django.core.mail import send_mail

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
    OpenApiResponse,
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .serializers import (
    FeedbackFormSerializer,
    FeedbackSuccessResponseSerializer,
    FeedbackErrorResponseSerializer,
    ThrottleErrorResponseSerializer,
)


@extend_schema(tags=['Forms group'])
@extend_schema_view(
    post=extend_schema(
        summary='Отправить форму обратной связи',
        description=(
            'Отправляет форму обратной связи и уведомляет администратора по '
            'email.\n\n'
            '**Лимит запросов:**\n'
            '• 100 запросов в день\n'
        ),
        request=FeedbackFormSerializer,
        responses={
            200: OpenApiResponse(
                response=FeedbackSuccessResponseSerializer,
                description='Форма успешно обработана и сообщение отправлено',
                examples=[
                    OpenApiExample(
                        'Успешная отправка',
                        value={
                            'status': 'success',
                            'message': 'Сообщение отправлено успешно!',
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                response=FeedbackErrorResponseSerializer,
                description='Ошибки валидации входных данных',
                examples=[
                    OpenApiExample(
                        'Ошибки валидации',
                        value={
                            'name': ['Обязательное поле.'],
                            'phone_number': [
                                'Неверный формат номера телефона'
                            ],
                            'message': ['Обязательное поле.'],
                            'accept_terms': [
                                'Необходимо принять условия обработки '
                                'персональных данных'
                            ],
                        },
                    )
                ],
            ),
            429: OpenApiResponse(
                response=ThrottleErrorResponseSerializer,
                description='Превышен лимит запросов (rate limiting)',
                examples=[
                    OpenApiExample(
                        'Rate limit exceeded',
                        value={
                            'detail': 'Request was throttled. Expected '
                            'available in 86400 seconds.'
                        },
                    )
                ],
            ),
        },
    )
)
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
