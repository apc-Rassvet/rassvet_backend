from rest_framework import serializers
from django.contrib.auth import get_user_model
from .. import models
from ..constants import REVIEW_TITLE_VALIDATE

User = get_user_model()


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = models.Review
        fields = [
            'id',
            'title',
            'content',
            'author_name',
            'created_at',
            'is_active'
        ]
        read_only_fields = ['created_at']
