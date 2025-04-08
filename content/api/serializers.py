from rest_framework import serializers
from django.contrib.auth import get_user_model
from .. import models

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


def validate_title(value):
    if len(value) < 5:
        raise serializers.ValidationError("Заголовок должен содержать минимум 5 символов")
    return value


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Review
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
