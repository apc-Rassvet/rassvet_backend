from rest_framework import viewsets, filters

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


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Video.objects.filter(is_active=True)
    serializer_class = serializers.VideoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


class TargetedFundraisingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.TargetedFundraising.objects.all()
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.TargetedFundraisingDetailSerializer
        return serializers.TargetedFundraisingListSerializer
