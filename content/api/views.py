from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from content import models
from content import pagination
from . import serializers


@extend_schema(tags=['Gratitudes group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Благодарностей.',
    ),
    retrieve=extend_schema(
        summary='Получить Благодарность по ID.',
    )
)
class GratitudeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получить все Благодарности списком, или конкретную по ID.
    """
    queryset = models.Gratitude.objects.filter(is_active=True)
    serializer_class = serializers.GratitudeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    pagination_class = pagination.GratitudePagination


@extend_schema(tags=['Partners group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список карточек Сотрудников.',
    ),
    retrieve=extend_schema(
        summary='Получить карточку Сотрудника по ID.',
    )
)
class PartnersViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получить все карточки Сотрудников списком, или конкретную по ID.
    """
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnersSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    pagination_class = LimitOffsetPagination


@extend_schema(tags=['Reviews group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Отзывов.',
    ),
    retrieve=extend_schema(
        summary='Получить Отзыв по ID.',
    )
)
class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получить все Отзывы списком, или конкретный по его ID.
    """
    queryset = models.Review.objects.filter(is_active=True)
    serializer_class = serializers.ReviewSerializer
    pagination_class = pagination.ReviewPagination
    ordering = ['-created_at']


@extend_schema(tags=['Videos group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Видео.',
    ),
    retrieve=extend_schema(
        summary='Получить Видео по ID.',
    )
)
class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получить все Видео списком, или конкретное по его ID.
    """
    queryset = models.Video.objects.filter(is_active=True)
    serializer_class = serializers.VideoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


@extend_schema(tags=['Fundraisings group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список Адресных сборов.',
        description='''
        Получить список Адресных сборов с достаточной информацией о сборе.
        ''',
    ),
    retrieve=extend_schema(
        summary='Получить Адресный сбор по ID.',
        description='''
        Получить Адресный сбор по ID с полной информацией о сборе.
        '''
    )
)
class TargetedFundraisingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получить список Адресных сборов, или конкретный по его ID.
    """
    queryset = models.TargetedFundraising.objects.all()
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.TargetedFundraisingDetailSerializer
        return serializers.TargetedFundraisingListSerializer
