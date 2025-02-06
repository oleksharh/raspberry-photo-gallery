import os

from django.db import models
from django.contrib.auth.models import User

# Album model
# NOTE: The shared_with field is a ManyToManyField to the User model
# This allows multiple users to be shared an album
# also, users that are not in shared_with can't access the album
class Album(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ['-created_at']


# Media model
# media files are uploaded to the media/ directory
# media files aren't stored in the database, only the path to the file
# in settings.py, the MEDIA_URL and MEDIA_ROOT settings are configured
# you can change them to suit your needs

def media_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    media_type = instance.media_type if instance.media_type else 'unknown'

    if media_type == 'image':
        return f'images/{filename}'
    elif media_type == 'video':
        return f'videos/{filename}'
    return f'other/{filename}'

class Media(models.Model):

    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to=media_upload_path)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    media_type = models.CharField(max_length=10, null=True)

    class Meta:
        ordering = ['-uploaded_at']
