from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Movies, Collection

class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserCreationSerializer, self).create(validated_data)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['uuid', 'title', 'description', 'genres']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'user', 'movies']

class GetCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description']

