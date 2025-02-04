from gallery.models import Album, Media
from gallery.serializers import AlbumSerializer, MediaSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser


class UserList(generics.ListAPIView):
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


class MediaList(generics.ListCreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    parser_classes = (MultiPartParser, FormParser)

class MediaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

class MediaCreate(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    parser_classes = [MultiPartParser, FormParser]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from gallery.permissions import IsAlbumSharedWith

class AlbumDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAlbumSharedWith]

    def get(self, request, album_id):
        try:
            album = Album.objects.get(id=album_id)
            self.check_object_permissions(request, album)  # Ensure user has permission
            return Response({'name': album.name, 'description': album.description})
        except Album.DoesNotExist:
            return Response({'error': 'Album not found'}, status=status.HTTP_404_NOT_FOUND)