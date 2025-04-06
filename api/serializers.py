from rest_framework import serializers
from .models import AddressCollection, CollectionPhoto, CollectionTextBlock, Partner


class AddressCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressCollection
        fields = '__all__'


class CollectionPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionPhoto
        fields = '__all__'


class CollectionTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionTextBlock
        fields = '__all__'


class PartnerSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = ['id', 'name', 'logo', 'logo_url', 'description', 'created_at', 'updated_at']
        extra_kwargs = {
            'logo': {'write_only': True},
        }

    def get_logo_url(self, obj):
        if obj.logo and hasattr(obj.logo, 'url'):
            return self.context['request'].build_absolute_uri(obj.logo.url)
        return None


class PartnerCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['name', 'logo', 'description']
