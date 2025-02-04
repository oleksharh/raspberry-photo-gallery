from rest_framework import permissions
from gallery.models import Album

class IsAlbumSharedWith(permissions.BasePermission):
    """
    Custom permission to allow access only to users an album is shared with.
    """
    
    def has_permission(self, request, view):
        # Allow authenticated users to check object-level permission
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow only users in the album's shared_with field
        if isinstance(obj, Album):
            return request.user in obj.shared_with.all() or request.user.is_superuser
        return False