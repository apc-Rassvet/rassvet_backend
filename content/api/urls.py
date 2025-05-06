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
v1_router_api.register(
    r'aba-therapy', views.HelpKidsViewSet, basename='aba-therapy'
)
v1_router_api.register(
    r'adaptive-physical-culture',
    views.HelpKidsViewSet,
    basename='adaptive-physical-culture',
)
v1_router_api.register(
    r'creative-workshops', views.HelpKidsViewSet, basename='creative-workshops'
)
v1_router_api.register(
    r'resource-classes', views.HelpKidsViewSet, basename='resource-classes'
)
v1_router_api.register(
    r'children-leisure', views.HelpKidsViewSet, basename='children-leisure'
)

api_urls.extend(v1_router_api.urls)

urlpatterns = [
    path('v1/', include(api_urls)),
]
