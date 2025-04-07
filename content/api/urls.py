from django.urls import include, path
from rest_framework import routers

from . import views


api_urls: list = []
v1_router_api = routers.DefaultRouter()
v1_router_api.register('videos', views.VideoViewSet, basename='video')
v1_router_api.register('gratitudes', views.GratitudeViewSet, basename='gratitude')
v1_router_api.register('collections', views.AddressCollectionViewSet, basename='collection')
v1_router_api.register('photos', views.CollectionPhotoViewSet, basename='photo')
v1_router_api.register('text-blocks', views.CollectionTextBlockViewSet, basename='text-block')

api_urls.extend(v1_router_api.urls)

urlpatterns = [
    path('v1/', include(api_urls)),
]
