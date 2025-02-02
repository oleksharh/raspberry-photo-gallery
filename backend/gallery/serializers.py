from rest_framework import serializers
from gallery.models import Album, Photo, Video
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # albums = serializers.PrimaryKeyRelatedField(many=True, queryset=Album.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username']

# TODO: CHECK SOME TUTORIALS ON HOW DJANGO REST FRAMEWORK WORKS, BECAUSE I AM NOT SURE IF THIS IS THE RIGHT WAY TO DO IT
# USERSERUIALIZER should work in views when listing, but it didn't change the model's meta in the db itself
# SHOULD WORK WITH gallery_album_shared_with table that connects user and album, have no clue how to implement it though


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