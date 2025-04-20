from django.urls import include, path
from rest_framework import routers

from . import views


api_urls: list = []
v1_router_api = routers.DefaultRouter()
v1_router_api.register(
    r'fundraisings', views.TargetedFundraisingViewSet, basename='fundraisings'
)
v1_router_api.register(
    r'gratitudes', views.GratitudeViewSet, basename='gratitude'
)
v1_router_api.register(r'partners', views.PartnersViewSet, basename='partner')
v1_router_api.register(r'reviews', views.ReviewViewSet, basename='review')
v1_router_api.register(
    r'about-video', views.AboutUsVideoViewSet, basename='about-video'
)

api_urls.extend(v1_router_api.urls)

urlpatterns = [
    path('v1/', include(api_urls)),
]
