from rest_framework import serializers

from .. import models


class GratitudeSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Gratitude
        fields = [
            'id',
            'title',
            'content',
            'file',
            'file_url',
            'created_at',
            'updated_at',
            'order',
        ]

    def get_file_url(self, obj) -> str | None:
        """
        Формирует абсолютный URL для файла, если он существует.
        """
        if obj.file:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = [
            'id',
            'title',
            'url',
            'description',
            'created_at',
            'is_active',
        ]


class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Partners
        fields = [
            'id',
            'name',
            'logo',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mission
        fields = [
            'mission_text',
            'ambitions_text',
            'five_year_goal',
            'tasks_text',
            'updated_at'
        ]
        read_only_fields = ['updated_at']
