from rest_framework import viewsets, filters, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .. import models
from .. import pagination
from . import serializers

User = get_user_model()


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


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Review.objects.filter(is_active=True)
    serializer_class = serializers.ReviewSerializer
    pagination_class = pagination.GratitudePagination
    ordering = ['-created_at']
