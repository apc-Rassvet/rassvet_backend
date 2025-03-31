from rest_framework import viewsets, filters
from api.models import Video, Gratitude
from api.pagination import StandardPagination
from api.serializers import VideoSerializer, GratitudeSerializer


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.filter(is_active=True)
    serializer_class = VideoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


class GratitudeViewSet(viewsets.ModelViewSet):
    queryset = Gratitude.objects.filter(is_active=True)
    serializer_class = GratitudeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    pagination_class = StandardPagination
