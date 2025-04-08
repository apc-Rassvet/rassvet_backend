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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
