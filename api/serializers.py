from rest_framework import serializers
from api.models import Gratitude, Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "url",
            "description",
            "created_at",
            "is_active",
        ]


class GratitudelSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Gratitude
        fields = [
            "id",
            "title",
            "content",
            "author",
            "file",
            "file_url",
            "created_at",
            "updated_at",
            "order",
        ]

    def get_file_url(self, obj):
        """
        Формирует абсолютный URL для файла, если он существует.
        """
        if obj.file:
            request = self.context.get("request")
            if request is not None:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
