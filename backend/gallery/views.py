from gallery.models import Album, Photo, Video
from gallery.serializers import AlbumSerializer, PhotoSerializer, VideoSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions


class UserList(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AlbumListCreate(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    # NOTE: Only admin can delete an album, i.e. superuser
    # TODO: Add permission to allow only the admin to delete an album


class AlbumDetail(generics.RetrieveUpdateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    # NOTE: Only admin can delete an album, i.e. superuser
    # TODO: Add permission to allow only the admin to delete an album


class PhotoList(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    # NOTE: Only admin and owner can delete a photo, i.e. superuser and the user who uploaded the photo
    # TODO: Add permission to allow only the owner or admin to delete a photo


class VideoListCreate(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    # NOTE: Only admin and owner can delete a video, i.e. superuser and the user who uploaded the video
    # TODO: Add permission to allow only the owner or admin to delete a video
