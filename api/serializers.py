from rest_framework import serializers
from .models import Document, Team


class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации о документах."""

    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ('id', 'name', 'file_url')

    def get_file_url(self, obj):
        return obj.file.url


class TeamSerializer(serializers.ModelSerializer):
    """Сериализаор для вывода информации о команде."""
    
    documents = DocumentSerializer(many=True)
    telefone = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Team
        fields = ('id', 'name', 'position', 'telephone', 'image', 'documents')
