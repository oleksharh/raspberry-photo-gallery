from django.db import models
from django.contrib.auth.models import User

# Album model
# NOTE: The shared_with field is a ManyToManyField to the User model
# This allows multiple users to be shared an album
# also, users that are not in shared_with can't access the album
class Album(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ['-created']


# Media model
# media files are uploaded to the media/ directory
# media files aren't stored in the database, only the path to the file
# in settings.py, the MEDIA_URL and MEDIA_ROOT settings are configured
# you can change them to suit your needs
class Media(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='media/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

# TODO: Add subdivision of media when stored in the database as well in the album
# when accessed. media/videos, media/images and album has two folders when being viewed
