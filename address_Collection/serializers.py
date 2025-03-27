from rest_framework import serializers

from .models import AddressCollection, CollectionPhoto, CollectionTextBlock


class CollectionPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionPhoto
        fields = '__all__'


class CollectionTextBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionTextBlock
        fields = '__all__'


class AddressCollectionSerializer(serializers.ModelSerializer):
    photos = CollectionPhotoSerializer(many=True, read_only=True)
    text_blocks = CollectionTextBlockSerializer(many=True, read_only=True)

    class Meta:
        model = AddressCollection
        fields = '__all__'
