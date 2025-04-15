from django.urls import path, include
from rest_framework import routers

from .views import TeamListView, TeamDetailView

# router = routers.DefaultRouter()
# router.register(r'teams', TeamListView)

urlpatterns = [
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
]