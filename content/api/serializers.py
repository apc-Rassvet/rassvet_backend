from rest_framework import serializers

from content import models


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


class AddressCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TargetedFundraising
        fields = '__all__'
