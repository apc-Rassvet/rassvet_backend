from django.urls import include, path
from rest_framework import routers

from api.views import GratitudeViewSet, VideoViewSet


api_urls = []
router_api = routers.DefaultRouter()
router_api.register('video', VideoViewSet, basename='video')
router_api.register('gratitude', GratitudeViewSet, basename='gratitude')

api_urls.extend(api_urls)

urlpatterns = [
    path('', include(api_urls)),
]
