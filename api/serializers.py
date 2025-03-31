from rest_framework import serializers
from .models import  AddressCollection, CollectionPhoto, CollectionTextBlock


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
