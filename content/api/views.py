from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

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
