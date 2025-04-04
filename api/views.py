from rest_framework import generics

from .models import Team
from .serializers import TeamSerializer, TeamDetailSerializer


class TeamListView(generics.ListAPIView):
    """Вьюсет для вывода информации о команде."""
    
    queryset = Team.objects.all().order_by('paginate')
    serializer_class = TeamSerializer

class TeamDetailView(generics.RetrieveAPIView):
    """Вьюсет для вывода информации о команде."""
    
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer