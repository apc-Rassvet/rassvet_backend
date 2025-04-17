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

    def get_specialities(self, obj):
        specialities_list = []
        specialities = obj.specialities.all().values(
            'speciality'
        ).order_by('position')
        for speciality in specialities:
            specialities_list.append(speciality['speciality'])
        return specialities_list

    def get_education(self, obj):
        education_list = []
        education = obj.education.all().values(
            'education'
        ).order_by('position')
        for i in education:
            education_list.append(i['education'])
        return education_list

    def get_additional_education(self, obj):
        additional_education_list = []
        additional_education = obj.additional_education.all().values(
            'additional_education'
        ).order_by('position')
        for i in additional_education:
            additional_education_list.append(i['additional_education'])
        return additional_education_list

    def get_trainings(self, obj):
        trainings_list = []
        trainings = obj.trainings.all().values(
            'trainings'
        ).order_by('position')
        for i in trainings:
            trainings_list.append(i['trainings'])
        return trainings_list

    def get_main_documents(self, obj):
        if obj.category_on_main:
            return obj.documents.filter(
                team_member=self.instance,
                on_main_page=True
            ).values_list('file', flat=True)
        else:
            return obj.documents.filter(
                team_member=self.instance
            ).values_list('file', flat=True)

    def get_category_documents(self, obj):
        if obj.category_on_main:
            categories = obj.documents.filter(
                team_member=self.instance
            ).values_list('type', flat=True).distinct()
            documents = {}
            documents['categorys'] = categories
            for category in categories:
                documents[category] = obj.documents.filter(
                    team_member=self.instance,
                    type=category
                ).values_list('file', flat=True)
            return documents
        else:
            return [None]
