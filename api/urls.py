from django.urls import path, include
from rest_framework import routers

from .views import TeamViewSet

router = routers.DefaultRouter()
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]