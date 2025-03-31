from rest_framework import viewsets

from .models import AddressCollection, CollectionPhoto, CollectionTextBlock
from .serializers import (
    AddressCollectionSerializer,
    CollectionPhotoSerializer,
    CollectionTextBlockSerializer,
)


class AddressCollectionViewSet(viewsets.ModelViewSet):
    queryset = AddressCollection.objects.all().order_by('order')
    serializer_class = AddressCollectionSerializer
    filterset_fields = ['status']


class CollectionPhotoViewSet(viewsets.ModelViewSet):
    queryset = CollectionPhoto.objects.all()
    serializer_class = CollectionPhotoSerializer


class CollectionTextViewSet(viewsets.ModelViewSet):
    queryset = CollectionTextBlock.objects.all()
    serializer_class = CollectionTextBlockSerializer


from django.shortcuts import render

# Create your views here.
