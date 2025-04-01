from rest_framework import viewsets

from .models import Team
from .serializers import TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """Вьюсет для вывода информации о команде."""
    
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
