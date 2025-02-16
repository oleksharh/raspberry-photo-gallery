# Standard libraries
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied

# Third-party libraries
from django.contrib.auth.models import User

# Local app imports
from gallery.models import Album, Media
from gallery.serializers import AlbumSerializer, MediaSerializer, UserSerializer
from gallery.permissions import IsAlbumSharedWith


##########################################
##              Album Views             ##
##########################################
class BaseAlbumView(generics.GenericAPIView):
    """ Abstract base class to avoid duplication """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class AlbumListCreate(BaseAlbumView, generics.ListCreateAPIView):
    """ Handles listing and creating albums """

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Album.objects.all()
        return Album.objects.filter(owner=user) | Album.objects.filter(shared_with=user)


class BaseAlbumPermissionsMixin:
    """ Mixin to avoid redundant permission checks for Album objects """
    def get_album(self, album_id):
        album = get_object_or_404(Album, id=album_id)
        self.check_object_permissions(self.request, album)
        return album


class AlbumDetailView(BaseAlbumPermissionsMixin, APIView):
    permission_classes = [permissions.IsAuthenticated, IsAlbumSharedWith]

    def get(self, request, album_id):
        album = get_object_or_404(Album, id=album_id)
        self.check_object_permissions(request, album)
        return Response(AlbumSerializer(album).data)
#-----------------------------------------#


##########################################
##              Media Views             ##
##########################################
class BaseMediaView(generics.GenericAPIView):
    """ Abstract base class for Media views to avoid redundancy """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    parser_classes = [MultiPartParser, FormParser]


class AlbumMediaList(BaseMediaView, generics.ListAPIView):
    """ Lists media files in a specific album (by ID or name) """
    permission_classes = [permissions.IsAuthenticated]
    album = None

    def get_album(self):
        """ Helper method to fetch the album by ID or name """
        album_identifier = self.kwargs.get('album_identifier')
        if album_identifier.isdigit():  # If it's an ID
            album = Album.objects.filter(id=album_identifier).first()
        else:
            album = Album.objects.filter(name=album_identifier).first()
        return album

    def check_permissions(self, request):
        """ Override to check permission on the album """
        album = self.get_album()
        if not album:
            raise PermissionDenied('Album not found.')

        # Check if the user has permission for this album
        self.album = album
        if not self.album.shared_with.filter(id=request.user.id).exists() and not request.user.is_superuser:
            raise PermissionDenied('You do not have permission to view this album.')
        return super().check_permissions(request)

    def get_queryset(self):
        """ Fetch media for the specified album """
        album = self.get_album()
        if album:
            return Media.objects.filter(album=album)
        return Media.objects.none()


class MediaDetail(BaseMediaView, generics.RetrieveUpdateDestroyAPIView):
    """ Retrieves, updates, or deletes a media file """
    pass


class MediaCreate(BaseMediaView, generics.CreateAPIView):
    """ Creates a new media file """
    pass
#-----------------------------------------#

