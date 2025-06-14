"""Маршруты API для приложения content.

Этот модуль определяет маршруты для версии API v1, включая:
- TargetedFundraisingViewSet: целевые сборы.
- GratitudeViewSet: благодарности.
- MissionViewSet: миссии.
- PartnersViewSet: партнёры.
- ProjectViewSet: проекты.
- ReviewViewSet: отзывы.
- AboutUsVideoViewSet: видео «О нас».
- EmployeeViewSet: сотрудники.

Используется DefaultRouter из DRF для автоматической генерации URL-адресов.
"""

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
v1_router_api.register(r'mission', views.MissionViewSet, basename='mission')
v1_router_api.register(r'partners', views.PartnersViewSet, basename='partner')
v1_router_api.register(r'projects', views.ProjectViewSet, basename='project')
v1_router_api.register(r'reviews', views.ReviewViewSet, basename='review')
v1_router_api.register(
    r'about-video', views.AboutUsVideoViewSet, basename='about-video'
)
v1_router_api.register(
    r'employees', views.EmployeeViewSet, basename='employee'
)
v1_router_api.register(r'news', views.NewsViewSet, basename='news')
v1_router_api.register(
    r'directions', views.DirectionViewSet, basename='direction'
)
v1_router_api.register(r'report', views.ReportViewSet, basename='report')

api_urls.extend(v1_router_api.urls)

urlpatterns = [
    path('v1/', include(api_urls)),
]
