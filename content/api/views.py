from rest_framework import viewsets, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .. import models
from .. import pagination
from . import serializers


class GratitudeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Gratitude.objects.filter(is_active=True)
    serializer_class = serializers.GratitudeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    pagination_class = pagination.GratitudePagination


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Video.objects.filter(is_active=True)
    serializer_class = serializers.VideoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


class PartnersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Partners.objects.all()
    serializer_class = serializers.PartnersSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    pagination_class = LimitOffsetPagination


class MissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.MissionSerializer

    def get_queryset(self):
        return models.Mission.objects.all()

    def list(self, request, *args, **kwargs):
        instance = models.Mission.objects.first()
        if not instance:
            return Response(
                {'detail': 'Контент страницы "Миссия" еще не создан.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    retrieve = list
