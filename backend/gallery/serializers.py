from rest_framework import serializers
from gallery.models import Album, Photo, Video
from django.contrib.auth.models import User

# class UserSerializer(serializers.ModelSerializer):
#     albums = serializers.PrimaryKeyRelatedField(many=True, queryset=Album.objects.all())

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'albums']

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'