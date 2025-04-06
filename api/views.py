from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import AddressCollection, CollectionPhoto, CollectionTextBlock, Partner
from .serializers import (
    AddressCollectionSerializer,
    CollectionPhotoSerializer,
    CollectionTextSerializer, PartnerCreateUpdateSerializer, PartnerSerializer,
)


class AddressCollectionViewSet(viewsets.ModelViewSet):
    queryset = AddressCollection.objects.all().order_by('order')
    serializer_class = AddressCollectionSerializer
    filterset_fields = ['status']


class CollectionPhotoViewSet(viewsets.ModelViewSet):
    queryset = CollectionPhoto.objects.all()
    serializer_class = CollectionPhotoSerializer


class CollectionTextBlockViewSet(viewsets.ModelViewSet):
    queryset = CollectionTextBlock.objects.all()
    serializer_class = CollectionTextSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    permission_classes = [permissions.IsAdminUser]  # Только для администраторов

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PartnerCreateUpdateSerializer
        return PartnerSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public_list(self, request):
        """Публичный список партнеров (доступен всем)"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
