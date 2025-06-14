"""Представления для API приложения content.

Содержит представления для следующих моделей:
- Gratitude (благодарности)
- Mission (миссии)
- Partner (партнеры)
- Project (проекты)
- Review (отзывы)
- AboutUsVideo (видео о нас)
- TargetedFundraising (адресные сборы)
- Employee (сотрудники)

Используются только для чтения (GET-запросов).
"""

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from content import filters
from content.models import (
    AboutUsVideo,
    Chapter,
    Direction,
    Employee,
    Gratitude,
    Mission,
    News,
    Partner,
    Project,
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


@extend_schema(tags=['Projects group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Проектов.',
    ),
    retrieve=extend_schema(
        summary='Получить Проект по ID.',
    ),
)
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Получить список Проектов, или конкретный по его ID."""

    queryset = (
        Project.objects.select_related('source_financing', 'program')
        .prefetch_related('photo')
        .all()
    )
    serializer_class = serializers.ProjectSerializer


@extend_schema(tags=['Missions group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить Миссию.',
    ),
)
class MissionViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Получить Миссию."""

    serializer_class = serializers.MissionSerializer

    def list(self, request, *args, **kwargs):
        """Возвращает единственную Миссию'.

        Если Миссия не найдена, возвращает 404.
        """
        mission = Mission.get_solo()
        if not mission:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(mission)
        return Response(serializer.data)


@extend_schema(tags=['News group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Новостей.',
    ),
    retrieve=extend_schema(
        summary='Получить Новость по ID.',
    ),
)
class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """Получить список Новостей, или конкретную по её ID."""

    queryset = News.objects.select_related('project').prefetch_related(
        'directions', 'gallery_images'
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NewsFilter

    def get_serializer_class(self):
        """Выбирает сериализатор в зависимости от действия.

        Возвращает краткий сериализатор для списка (list)
        и детальный для отдельного сотрудника (retrieve).
        """
        if self.action == 'retrieve':
            return serializers.NewsDetailSerializer
        return serializers.NewsSerializer


@extend_schema(tags=['Directions group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Направлений.',
    ),
    retrieve=extend_schema(
        summary='Получить Направление по ID.',
    ),
)
class DirectionViewSet(viewsets.ReadOnlyModelViewSet):
    """Получить список Направлений, или конкретное по его ID."""

    queryset = Direction.objects.all()
    serializer_class = serializers.DirectionSerializer


@extend_schema(tags=['Reports'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список отчетов.',
        description="""
        Получить список отчетов с сортировкой по разделам.
        """,
    ),
    retrieve=extend_schema(
        summary='Получить список отчетов раздела.',
        description="""
        Получить список отчетов одного раздела.
        """,
    ),
)
class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """Получить список отчетов, или конкретный по его ID."""

    queryset = Chapter.objects.prefetch_related('reports').all()
    serializer_class = serializers.ChapterSerializer
