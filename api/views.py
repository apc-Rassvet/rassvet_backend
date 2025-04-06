from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Mission
from .serializers import MissionSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'update']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_object(self):
        return Mission.objects.first()

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {'detail': 'Контент страницы "Миссия" еще не создан.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if Mission.objects.exists():
            return Response(
                {'detail': 'Контент миссии уже существует.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
