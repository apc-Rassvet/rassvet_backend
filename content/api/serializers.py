from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from content import models


class GratitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gratitude
        fields = [
            'id',
            'title',
            'description',
            'file',
            'order',
            'created_at',
            'updated_at',
        ]


class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Partner
        fields = [
            'id',
            'name',
            'logo',
            'description',
            'created_at',
            'updated_at',
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
            'is_active',
            'created_at',
            'updated_at',
        ]


class AboutUsVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AboutUsVideo
        fields = [
            'title',
            'url',
            'description',
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
    photos = FundraisingPhotoSerializer(many=True)
    text_blocks = FundraisingTextBlockSerializer(many=True)

    class Meta:
        model = models.TargetedFundraising
        fields = (
            'id',
            'title',
            'short_description',
            'status',
            'photos',
            'text_blocks',
            'order',
        )


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализаор для вывода информации о команде."""

    class Meta:
        model = models.Employee
        fields = ('id', 'name', 'image', 'main_specialities', 'order')


class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации о документах."""

    class Meta:
        model = models.Document
        fields = ('id', 'name', 'file')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации о категории."""

    documents = serializers.SerializerMethodField()

    class Meta:
        model = models.TypeDocument
        fields = ('id', 'name', 'documents')

    def get_documents(self, obj):
        document_obj = obj.documents.filter(
            employee=self.context.get('employee')
        )
        return DocumentSerializer(
            document_obj, many=True, context=self.context
        ).data


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации члене команды."""

    main_documents = serializers.SerializerMethodField()
    category_documents = serializers.SerializerMethodField()

    class Meta:
        model = models.Employee
        fields = (
            'id',
            'name',
            'specialities',
            'education',
            'additional_education',
            'trainings',
            'interviews',
            'specialists_register',
            'image',
            'main_documents',
            'category_documents',
        )

    @extend_schema_field(list[dict])
    def get_main_documents(self, obj) -> list[dict]:
        if obj.category_on_main:
            doc = models.Document.objects.filter(
                employee=self.instance, on_main_page=True
            )
            return DocumentSerializer(
                doc, many=True, context=self.context
            ).data
        else:
            doc = models.Document.objects.filter(employee=self.instance)
            return DocumentSerializer(
                doc, many=True, context=self.context
            ).data

    @extend_schema_field(list[dict])
    def get_category_documents(self, obj) -> list[dict]:
        if not obj.category_on_main:
            return []
        categories = models.TypeDocument.objects.filter(
            documents__employee=obj
        ).distinct()
        self.context['employee'] = obj
        return CategorySerializer(
            categories, many=True, context=self.context
        ).data
