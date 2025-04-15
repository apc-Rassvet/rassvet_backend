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
        """Формирует абсолютный URL для файла, если он существует."""
        if obj.file:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Partner
        fields = [
            'id',
            'name',
            'logo',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = [
            'id',
            'title',
            'content',
            'author_name',
            'created_at',
            'updated_at',
            'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at']


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


class FundraisingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundraisingPhoto
        fields = ('position', 'image')


class FundraisingTextBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundraisingTextBlock
        fields = ('position', 'title', 'content')


class TargetedFundraisingListSerializer(serializers.ModelSerializer):
    main_photo = serializers.SerializerMethodField()

    class Meta:
        model = models.TargetedFundraising
        fields = ('id', 'title', 'short_description', 'status', 'main_photo')

    def get_main_photo(self, obj):
        photo = obj.photos.filter(position=1).first()
        if photo:
            return FundraisingPhotoSerializer(photo, context=self.context).data
        return None


class TargetedFundraisingDetailSerializer(serializers.ModelSerializer):
    photos = FundraisingPhotoSerializer(many=True, read_only=True)
    text_blocks = FundraisingTextBlockSerializer(many=True, read_only=True)

    class Meta:
        model = models.TargetedFundraising
        fields = (
            'id',
            'title',
            'short_description',
            'status',
            'photos',
            'text_blocks',
        )

class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации о документах."""

    file_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Document
        fields = ('id', 'name', 'file_url', 'type')

    def get_file_url(self, obj):
        return obj.file.url


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализаор для вывода информации о команде."""

    class Meta:
        model = models.Employee
        fields = ('id', 'name', 'position', 'image')

class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации члене команды."""
    
    documents = serializers.SerializerMethodField()

    class Meta:
        model = models.Employee
        fields = ('id', 'name', 'position', 'image', 'documents')
    
    def get_documents(self, obj):
        if obj.category_on_main:
            main_documents = obj.documents.filter(
                team_member=self.instance, 
                on_main_page=True
            ).values_list('file', flat=True)
            category_documents = obj.documents.filter(
                team_member=self.instance
            ).values_list('type__type', flat=True).distinct()
            return main_documents, category_documents
        else:
            return obj.documents.filter(
                team_member=self.instance
            ).values_list('file', flat=True)

