# Standard libraries
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

# Third-party libraries
from django.contrib.auth.models import User

# Local app imports
from gallery.models import Album, Media
from gallery.serializers import AlbumSerializer, MediaSerializer, UserSerializer
from gallery.permissions import IsAlbumSharedWith


##########################################
##              User Views              ##  
##########################################
class BaseUserView(generics.GenericAPIView):
    """ Abstract base class to avoid duplication """
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList(BaseUserView, generics.ListCreateAPIView):
    """ Handles listing and creating users """
    pass


class UserDetail(BaseUserView, generics.RetrieveUpdateDestroyAPIView):
    """ Handles retrieving, updating, and deleting a user """
    pass
#-----------------------------------------#


##########################################
##              Album Views             ##
##########################################
class BaseAlbumView(generics.GenericAPIView):
    """ Abstract base class to avoid duplication """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class AlbumListCreate(BaseAlbumView, generics.ListCreateAPIView):
    """ Handles listing and creating albums """
    pass
    # NOTE: Only admin can delete an album, i.e. superuser
    # TODO: Add permission to allow only the admin to delete an album


class AlbumDetail(BaseAlbumView, generics.RetrieveUpdateAPIView):
    """ Handles retrieving and updating an album """

    # NOTE: Only admin can delete an album, i.e. superuser
    # TODO: Add permission to allow only the admin to delete an album


class BaseAlbumPermissionsMixin:
    """ Mixin to avoid redundant permission checks for Album objects """
    def get_album(self, album_id):
        try:
            album = Album.objects.get(id=album_id)
            self.check_object_permissions(self.request, album)  # Ensure user has permission
            return album
        except Album.DoesNotExist:
            return None


class AlbumDetailView(BaseAlbumPermissionsMixin, APIView):
    permission_classes = [permissions.IsAuthenticated, IsAlbumSharedWith]

    def get(self, request, album_id):
        album = self.get_album(album_id)
        if album:
            return Response({'name': album.name, 'description': album.description})
        return Response({'error': 'Album not found'}, status=status.HTTP_404_NOT_FOUND)
#-----------------------------------------#


##########################################
##              Media Views             ##
##########################################
class BaseMediaView(generics.GenericAPIView):
    """ Abstract base class for Media views to avoid redundancy """
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    parser_classes = [MultiPartParser, FormParser]


class MediaList(BaseMediaView, generics.ListAPIView):
    """ Lists all media files """
    pass


class MediaDetail(BaseMediaView, generics.RetrieveUpdateDestroyAPIView):
    """ Retrieves, updates, or deletes a media file """
    pass


class MediaCreate(BaseMediaView, generics.CreateAPIView):
    """ Creates a new media file """
    pass
#-----------------------------------------#

