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


class AddressCollectionViewSet(viewsets.ModelViewSet):
    queryset = models.AddressCollection.objects.all().order_by('order')
    serializer_class = serializers.AddressCollectionSerializer
    filterset_fields = ['status']


class CollectionPhotoViewSet(viewsets.ModelViewSet):
    queryset = models.CollectionPhoto.objects.all()
    serializer_class = serializers.CollectionPhotoSerializer


class CollectionTextBlockViewSet(viewsets.ModelViewSet):
    queryset = models.CollectionTextBlock.objects.all()
    serializer_class = serializers.CollectionTextSerializer
