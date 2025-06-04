"""Представления для API приложения content.

Содержит представления для следующих моделей:
- Gratitude (благодарности)
- Partner (партнеры)
- Review (отзывы)
- AboutUsVideo (видео о нас)
- TargetedFundraising (адресные сборы)
- Employee (сотрудники)

Используются только для чтения (GET-запросов).
"""
import os
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.conf import settings

from content.models import (
    AboutUsVideo,
    Employee,
    Gratitude,
    Partner,
    Review,
    TargetedFundraising,
)

from . import serializers


@extend_schema(tags=['Gratitudes group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Благодарностей.',
    ),
    retrieve=extend_schema(
        summary='Получить Благодарность по ID.',
    ),
)
class GratitudeViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение благодарностей.

    Используйте этот эндпоинт, чтобы отобразить благодарности.
    Можно получить как весь список, так и одну благодарность по ID.
    """

    queryset = Gratitude.objects.filter(is_active=True)
    serializer_class = serializers.GratitudeSerializer


@extend_schema(tags=['Partners group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список карточек Партнеров.',
    ),
    retrieve=extend_schema(
        summary='Получить карточку Партнера по ID.',
    ),
)
class PartnersViewSet(viewsets.ReadOnlyModelViewSet):
    """Информация о партнёрах.

    Используйте этот эндпоинт, чтобы отобразить информацию о партнёрах.
    Можно получить как весь список, так и одного партнёра по ID.
    """

    queryset = Partner.objects.all()
    serializer_class = serializers.PartnersSerializer


@extend_schema(tags=['Reviews group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Отзывов.',
    ),
    retrieve=extend_schema(
        summary='Получить Отзыв по ID.',
    ),
)
class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """Информация об отзывах.

    Используйте этот эндпоинт, чтобы отобразить информацию об отзывах.
    Можно получить как весь список, так и один отзыв по ID.
    """

    queryset = Review.objects.filter(is_active=True)
    serializer_class = serializers.ReviewSerializer


@extend_schema(tags=['VideoAboutUs group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить Видео.',
    )
)
class AboutUsVideoViewSet(viewsets.GenericViewSet):
    """Информация о видео об организации.

    Возвращает одно видео с названием и ссылкой на источник.
    Используется для блока "О нас".
    """

    serializer_class = serializers.AboutUsVideoSerializer

    def list(self, request, *args, **kwargs):
        """Возвращает единственное видео для блока 'О нас'.

        Если видео не найдено, возвращает 404.
        """
        video = AboutUsVideo.get_solo()
        if not video:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(video)
        return Response(serializer.data)


@extend_schema(tags=['Fundraisings group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Адресных сборов.',
        description="""
        Получить список Адресных сборов с достаточной информацией о сборе.
        """,
    ),
    retrieve=extend_schema(
        summary='Получить Адресный сбор по ID.',
        description="""
        Получить Адресный сбор по ID с полной информацией о сборе.
        """,
    ),
)
class TargetedFundraisingViewSet(viewsets.ReadOnlyModelViewSet):
    """Информация об адресных сборах.

    Используйте этот эндпоинт, чтобы отобразить информацию об адресных сборах.
    Можно получить как весь список, так и один адресный сбор по ID.
    """

    queryset = TargetedFundraising.objects.all()

    def get_serializer_class(self):
        """Выбирает сериализатор в зависимости от действия.

        Возвращает краткий сериализатор для списка (list)
        и детальный для отдельного сбора (retrieve).
        """
        if self.action == 'retrieve':
            return serializers.TargetedFundraisingDetailSerializer
        return serializers.TargetedFundraisingListSerializer


@extend_schema(tags=['Employees group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Сотрудников.',
    ),
    retrieve=extend_schema(
        summary='Получить карточку Сотрудника по ID.',
    ),
)
class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """Информация о сотрудниках.

    Используйте этот эндпоинт, чтобы отобразить информацию о сотрудниках.
    Можно получить как весь список, так и одного сотрудника по ID.
    """

    queryset = Employee.objects.all()

    def get_serializer_class(self):
        """Выбирает сериализатор в зависимости от действия.

        Возвращает краткий сериализатор для списка (list)
        и детальный для отдельного сотрудника (retrieve).
        """
        if self.action == 'retrieve':
            return serializers.EmployeeDetailSerializer
        return serializers.EmployeeSerializer


@extend_schema(tags=['FitbakForm view'])
@extend_schema_view(
    list=extend_schema(
        summary='Отравить сообщение на почту.',
    ),
    retrieve=extend_schema(
        summary=(
            'Отправить сообщение на почту с информацией обратной связи.'
            'Пример: {"name": "Имя", "phone_number": "+79999999999", "message": "Сообщение"}'
            'Возвращает статус 200, если сообщение отправлено успешно.'
        ),
    ),
)
class FitbakFormView(APIView):
    """Форма обратной связи."""
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request, *args, **kwargs):
        """Создание новой записи в базе данных."""
        serializer = serializers.FitbakFormSerializer(data=request.data)
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
                {'status': 'success', 'message': 'Сообщение отправлено успешно!'},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
