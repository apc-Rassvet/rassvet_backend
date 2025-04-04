from rest_framework import serializers
from .models import Document, Team


class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации о документах."""

    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ('id', 'name', 'file_url', 'type')

    def get_file_url(self, obj):
        return obj.file.url


class TeamSerializer(serializers.ModelSerializer):
    """Сериализаор для вывода информации о команде."""

    class Meta:
        model = Team
        fields = ('id', 'name', 'position', 'image')

class TeamDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации члене команды."""
    
    documents_type = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'name', 'position', 'image', 'documents', 'documents_type')
    
    def get_documents(self, obj):
        return obj.documents.filter(team_member=self.instance, on_main_page=True).values_list('file', flat=True)

    def get_documents_type(self, obj):
        return obj.documents.filter(team_member=self.instance).values_list('type__type', flat=True).distinct()