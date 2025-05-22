"""Сериализаторы для моделей приложения.

Этот модуль содержит сериализаторы, используемые для преобразования
данных моделей в JSON-формат для API, а также обработки входящих данных.

Включенные сериализаторы:
- GratitudeSerializer: для благодарностей.
- PartnersSerializer: для партнёров.
- ReviewSerializer: для отзывов.
- AboutUsVideoSerializer: для видео о нас.
- FundraisingPhotoSerializer: для фотографий сборов.
- FundraisingTextBlockSerializer: для текстовых блоков сборов.
- TargetedFundraisingListSerializer: краткий формат сбора средств.
- TargetedFundraisingDetailSerializer: детальный формат сбора средств.
- EmployeeSerializer: краткая информация о сотруднике.
- DocumentSerializer: документы сотрудников.
- CategorySerializer: категория документов сотрудника.
- EmployeeDetailSerializer: подробная информация о сотруднике с документами.
- ProjectPhotoSerializer: для фотографий проектов.
- ProjectSerializer: для проектов.
- MissionSerializer: для миссий.
"""

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from content.models import (
    AboutUsVideo,
    Direction,
    Document,
    Employee,
    FundraisingPhoto,
    FundraisingTextBlock,
    GalleryImage,
    Gratitude,
    Mission,
    News,
    Partner,
    Project,
    ProjectPhoto,
    Review,
    TargetedFundraising,
    TypeDocument,
)


class GratitudeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Gratitude."""

    class Meta:
        """Meta класс с настройками сериализатора Gratitude."""

        model = Gratitude
        fields = [
            'id',
            'title',
            'file',
            'order',
            'created_at',
            'updated_at',
        ]


class PartnersSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Partner."""

    class Meta:
        """Meta класс с настройками сериализатора Partner."""

        model = Partner
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
    """Сериализатор для модели Review."""

    class Meta:
        """Meta класс с настройками сериализатора Review."""

        model = Review
        fields = [
            'id',
            'author_name',
            'content',
            'order',
            'is_active',
            'created_at',
            'updated_at',
        ]


class AboutUsVideoSerializer(serializers.ModelSerializer):
    """Сериализатор для модели AboutUsVideo."""

    class Meta:
        """Meta класс с настройками сериализатора AboutUsVideo."""

        model = AboutUsVideo
        fields = [
            'title',
            'url',
        ]


class FundraisingPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор для фотографий, связанных с TargetedFundraising."""

    class Meta:
        """Meta класс с настройками сериализатора FundraisingPhoto."""

        model = FundraisingPhoto
        fields = ('title', 'position', 'image')


class FundraisingTextBlockSerializer(serializers.ModelSerializer):
    """Сериализатор для текстовых блоков, связанных с TargetedFundraising."""

    class Meta:
        """Meta класс с настройками сериализатора FundraisingTextBlock."""

        model = FundraisingTextBlock
        fields = ('position', 'content')


class TargetedFundraisingListSerializer(serializers.ModelSerializer):
    """Сериализатор списка адресных сборов (TargetedFundraising)."""

    main_photo = serializers.SerializerMethodField()

    class Meta:
        """Meta класс с настройками сериализатора TargetedFundraising."""

        model = TargetedFundraising
        fields = (
            'id',
            'title',
            'short_description',
            'status',
            'main_photo',
            'created_at',
            'updated_at',
        )

    @extend_schema_field(FundraisingPhotoSerializer(allow_null=True))
    def get_main_photo(self, obj):
        """Возвращает главное фото для сбора (position=1)."""
        photo = obj.photos.filter(position=1).first()
        if photo:
            return FundraisingPhotoSerializer(photo, context=self.context).data
        return None


class TargetedFundraisingDetailSerializer(serializers.ModelSerializer):
    """Детализированный сериализатор для TargetedFundraising.

    Включает в себя все фото, текстовые блоки и другие подробности сбора.
    """

    photos = FundraisingPhotoSerializer(many=True)
    text_blocks = FundraisingTextBlockSerializer(many=True)

    class Meta:
        """Meta класс с настройками сериализатора TargetedFundraising."""

        model = TargetedFundraising
        fields = (
            'id',
            'title',
            'short_description',
            'fundraising_link',
            'status',
            'photos',
            'text_blocks',
            'order',
        )


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого отображения информации о сотруднике."""

    class Meta:
        """Meta класс с настройками сериализатора Employee."""

        model = Employee
        fields = (
            'id',
            'name',
            'image',
            'main_specialities',
            'order',
            'created_at',
            'updated_at',
        )


class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Document."""

    class Meta:
        """Meta класс с настройками сериализатора Document."""

        model = Document
        fields = ('id', 'name', 'file')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий документов (TypeDocument).

    Добавляет поле documents, отфильтрованное по текущему сотруднику.
    """

    documents = serializers.SerializerMethodField()

    class Meta:
        """Meta класс с настройками сериализатора TypeDocument."""

        model = TypeDocument
        fields = ('id', 'name', 'documents')

    def get_documents(self, obj):
        """Возвращает документы для конкретного сотрудника и категории."""
        document_obj = obj.documents.filter(
            employee=self.context.get('employee')
        )
        return DocumentSerializer(
            document_obj, many=True, context=self.context
        ).data


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Детализированный сериализатор для модели Employee.

    Включает основной список документов и документы по категориям.
    """

    main_documents = serializers.SerializerMethodField()
    category_documents = serializers.SerializerMethodField()

    class Meta:
        """Meta класс с настройками сериализатора Employee."""

        model = Employee
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
        """Возвращает список документов сотрудника отображаемых в ленте."""
        if obj.category_on_main:
            document = Document.objects.filter(
                employee=self.instance, on_main_page=True
            )
            return DocumentSerializer(
                document, many=True, context=self.context
            ).data
        document = Document.objects.filter(employee=self.instance)
        return DocumentSerializer(
            document, many=True, context=self.context
        ).data

    @extend_schema_field(list[dict])
    def get_category_documents(self, obj) -> list[dict]:
        """Возвращает документы, сгруппированные по категориям."""
        if not obj.category_on_main:
            return []
        categories = TypeDocument.objects.filter(
            documents__employee=obj
        ).distinct()
        self.context['employee'] = obj
        return CategorySerializer(
            categories, many=True, context=self.context
        ).data


class ProjectPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор ProjectPhoto."""

    class Meta:
        """Meta класс с настройками сериализатора ProjectPhotoSerializer."""

        model = ProjectPhoto
        fields = ('image',)


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализатор Project."""

    photo = ProjectPhotoSerializer(many=True)
    program = serializers.CharField(source='program.title')
    source_financing = serializers.CharField(source='source_financing.name')

    class Meta:
        """Meta класс с настройками сериализатора ProjectSerializer."""

        model = Project
        fields = (
            'id',
            'order',
            'title',
            'logo',
            'status',
            'project_start',
            'project_end',
            'source_financing',
            'project_rassvet',
            'program',
            'photo',
            'project_goal',
            'project_tasks',
            'project_description',
            'achieved_results',
        )


class MissionSerializer(serializers.ModelSerializer):
    """Сериализатор Mission."""

    class Meta:
        """Meta класс с настройками сериализатора MissionSerializer."""

        model = Mission
        fields = (
            'id',
            'order',
            'organization_mission',
            'ambitions',
            'goal_for_five_years',
            'tasks',
        )


class DirectionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели направления деятельности."""

    class Meta:
        """Meta класс с настройками сериализатора DirectionSerializer."""

        model = Direction
        fields = ('id', 'name')


class GalleryImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений галереи."""

    class Meta:
        """Meta класс с настройками сериализатора GalleryImageSerializer."""

        model = GalleryImage
        fields = ('id', 'name', 'image', 'order')


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели новости на общей странице."""

    directions = DirectionSerializer(many=True, read_only=True)

    class Meta:
        """Meta класс с настройками сериализатора NewsSerializer."""

        model = News
        fields = (
            'id',
            'title',
            'summary',
            'date',
            'photo',
            'show_on_main',
            'directions',
        )


class NewsDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для модели новости на подробной странице."""

    directions = DirectionSerializer(many=True, read_only=True)
    project = ProjectSerializer(read_only=True)
    gallery_images = GalleryImageSerializer(many=True, read_only=True)

    class Meta:
        """Meta класс с настройками сериализатора NewsDetailSerializer."""

        model = News
        fields = (
            'id',
            'title',
            'photo',
            'date',
            'course_start',
            'summary',
            'detail_page_type',
            'detail_page_link',
            'show_on_main',
            'full_text',
            'video_url',
            'directions',
            'project',
            'gallery_images',
            'created_at',
            'updated_at',
        )
