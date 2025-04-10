from django.urls import include, path
from rest_framework import routers

from . import views


api_urls: list = []
v1_router_api = routers.DefaultRouter()
v1_router_api.register('videos', views.VideoViewSet, basename='video')
v1_router_api.register(
    'gratitudes', views.GratitudeViewSet, basename='gratitude'
)
v1_router_api.register(
    'fundraisings', views.TargetedFundraisingViewSet, basename='fundraisings'
)
api_urls.extend(v1_router_api.urls)

urlpatterns = [
    path('v1/', include(api_urls)),
]
