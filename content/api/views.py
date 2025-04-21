from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from content import models
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


@extend_schema(tags=['Partners group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список карточек Партнеров.',
    ),
    retrieve=extend_schema(
        summary='Получить карточку Партнера по ID.',
    )
)
class PartnersViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получить все карточки Партнеров списком, или конкретную по ID.
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


@extend_schema(tags=['VideoAboutUs group'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить Видео.',
    )
)
class AboutUsVideoViewSet(viewsets.GenericViewSet):
    """
    Получить Видео для раздела 'О нас'.
    """
    serializer_class = serializers.AboutUsVideoSerializer

    def list(self, request, *args, **kwargs):
        video = models.AboutUsVideo.get_solo()
        if not video:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(video)
        return Response(serializer.data)


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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.TargetedFundraisingDetailSerializer
        return serializers.TargetedFundraisingListSerializer
