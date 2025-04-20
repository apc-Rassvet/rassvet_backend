from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from content import models
from . import serializers


class GratitudeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Gratitude.objects.filter(is_active=True)
    serializer_class = serializers.GratitudeSerializer


class PartnersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnersSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer


class AboutUsVideoViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.AboutUsVideoSerializer

    def list(self, request, *args, **kwargs):
        video = models.AboutUsVideo.get_solo()
        if not video:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(video)
        return Response(serializer.data)


class TargetedFundraisingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.TargetedFundraising.objects.all()
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    filterset_fields = ['status']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.TargetedFundraisingDetailSerializer
        return serializers.TargetedFundraisingListSerializer
