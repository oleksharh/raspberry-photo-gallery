# Standard libraries
from rest_framework import generics, permissions

# Third-party libraries
from django.contrib.auth.models import User

# Local app imports
from gallery.serializers import UserSerializer


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

