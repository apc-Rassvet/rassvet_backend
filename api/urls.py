from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    AddressCollectionViewSet,
    CollectionPhotoViewSet,
    CollectionTextBlockViewSet
)

router = DefaultRouter()
router.register(r'collections', AddressCollectionViewSet, basename='collection')
router.register(r'photos', CollectionPhotoViewSet, basename='photo')
router.register(r'text-blocks', CollectionTextBlockViewSet, basename='text-block')

urlpatterns = [
    path('', include(router.urls)),
]
