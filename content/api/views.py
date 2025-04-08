from rest_framework import viewsets, filters

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


class PartnersViewSet(viewsets.ModelViewSet):
    queryset = models.Partners.objects.all()
    serializer_class = serializers.PartnersSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
