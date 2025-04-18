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


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализаор для вывода информации о команде."""

    specialities = serializers.SerializerMethodField()

    class Meta:
        model = models.Employee
        fields = ('id', 'name', 'image', 'specialities')

    def queryset(self):
        return models.Employee.objects.all().order_by('ordaring', 'name')

    def get_specialities(self, obj):
        specialities_list = []
        specialities = obj.specialities.filter(
            on_main=True
        ).values('speciality').order_by('position')
        for speciality in specialities:
            specialities_list.append(speciality['speciality'])
        return specialities_list


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации члене команды."""

    specialities = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    main_documents = serializers.SerializerMethodField()
    category_documents = serializers.SerializerMethodField()
    additional_education = serializers.SerializerMethodField()
    trainings = serializers.SerializerMethodField()

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
            'image',
            'main_documents',
            'category_documents'
        )

    def make_list(self, model, field):
        field_list = []
        list = model.all().values(
            field
        ).order_by('position')
        for i in list:
            field_list.append(i[field])
        return field_list

    def get_specialities(self, obj):
        field = 'speciality'
        return self.make_list(obj.specialities, field)

    def get_education(self, obj):
        field = 'education'
        return self.make_list(obj.education, field)

    def get_additional_education(self, obj):
        field = 'additional_education'
        return self.make_list(obj.additional_education, field)

    def get_trainings(self, obj):
        field = 'trainings'
        return self.make_list(obj.trainings, field)

    def build_url(self, request, documents):
        if request is not None:
            documents_url = []
            for document in documents:
                documents_url.append(request.build_absolute_uri(document))
            return documents_url
        return documents

    def get_main_documents(self, obj):
        request = self.context.get('request')
        if obj.category_on_main:
            documents = obj.documents.filter(
                team_member=self.instance,
                on_main_page=True
            ).values_list('file', flat=True)
            return self.build_url(request, documents)
        else:
            documents = obj.documents.filter(
                team_member=self.instance
            ).values_list('file', flat=True)
            return self.build_url(request, documents)

    def get_category_documents(self, obj):
        request = self.context.get('request')
        if obj.category_on_main:
            categories = obj.type_documents.filter(
                team_member=self.instance
            ).values_list('name', flat=True)
            documents = {}
            documents['categorys'] = categories
            for category in categories:
                doc = obj.documents.filter(
                    team_member=self.instance,
                    type__name=category
                ).values_list('file', flat=True)
                documents[category] = self.build_url(request, doc)
            return documents
        else:
            return [None]
