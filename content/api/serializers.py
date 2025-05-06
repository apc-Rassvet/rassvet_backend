from rest_framework import serializers

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


class SupervisorSerializer(serializers.ModelSerializer):
    """Сериализатор для супервизоров"""

    class Meta:
        model = models.Supervisor
        fields = ('id', 'name', 'position', 'image', 'ordering')
