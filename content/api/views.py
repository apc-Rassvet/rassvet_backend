from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import extend_schema, extend_schema_view

from content import models
from content import pagination
from . import serializers


class GratitudeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Gratitude.objects.filter(is_active=True)
    serializer_class = serializers.GratitudeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    pagination_class = pagination.GratitudePagination


class PartnersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnersSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Review.objects.filter(is_active=True)
    serializer_class = serializers.ReviewSerializer
    pagination_class = pagination.ReviewPagination
    ordering = ['-created_at']


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Video.objects.filter(is_active=True)
    serializer_class = serializers.VideoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


@extend_schema(tags=["Test group."])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список.",
        # description="""Описание list.""",
    ),
    retrieve=extend_schema(
        summary="Получить по id.",
        # description="""Описание retrieve.""",
    )
)
class TargetedFundraisingViewSet(viewsets.ReadOnlyModelViewSet):
    """Описание для всех list + retrieve +.. ."""
    queryset = models.TargetedFundraising.objects.all()
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.TargetedFundraisingDetailSerializer
        return serializers.TargetedFundraisingListSerializer
