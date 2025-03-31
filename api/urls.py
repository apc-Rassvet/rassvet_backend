from django.urls import path

from .views import (
    AddressCollectionViewSet,
    CollectionPhotoViewSet,
    CollectionTextViewSet,
)

urlpatterns = [
    path('collections/', AddressCollectionViewSet.as_view({'get': 'list', 'post': 'create'}), name='collection-list'),
    path('collections/<int:pk>/', AddressCollectionViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                                    'delete': 'destroy'}), name='collection-detail'),
    path('photos/', CollectionPhotoViewSet.as_view({'get': 'list', 'post': 'create'}), name='photo-list'),
    path('photos/<int:pk>/', CollectionPhotoViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                             'delete': 'destroy'}), name='photo-detail'),
    path('text-blocks/', CollectionTextViewSet.as_view({'get': 'list', 'post': 'create'}), name='text-block-list'),
    path('text-blocks/<int:pk>/', CollectionTextViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                                 'delete': 'destroy'}), name='text-block-detail'),
]