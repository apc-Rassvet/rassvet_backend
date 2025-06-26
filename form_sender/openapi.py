"""OpenAPI схемы для приложения forms."""

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
    OpenApiResponse,
)

from .serializers import (
    FeedbackFormSerializer,
    FeedbackSuccessResponseSerializer,
    FeedbackErrorResponseSerializer,
    ThrottleErrorResponseSerializer,
)


feedback_form_schema = extend_schema_view(
    post=extend_schema(
        summary='Отправить форму обратной связи',
        description=(
            'Отправляет форму обратной связи и уведомляет администратора по '
            'email.\n\n'
            '**Лимит запросов:**\n'
            '• 30 запросов в час\n'
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
