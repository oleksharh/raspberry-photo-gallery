from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ['-created']


class Media(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='media/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
