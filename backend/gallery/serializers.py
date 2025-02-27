import os

from rest_framework import serializers
from gallery.models import Album, Media
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Prevents password from being exposed

    def update(self, instance, validated_data):
        # Handle password hashing during updates
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Securely hash password
            validated_data.pop('password', None)  # Remove password from validated data
        return super().update(instance, validated_data)


# Custom validator to ensure only certain file types are uploaded

class MediaSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Media
        fields = ['album', 'file', 'uploaded_at']  # Include all fields from the Media model

    def validate_file(self, value):
        allowed_types = {
            'image': {'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/heif', 'image/heic'},
            'video': {'video/mp4', 'video/avi', 'video/mkv', 'video/webm'},
        }
        
        file_type = value.content_type.split('/')[0]  # Extract 'image' or 'video'
        
        if value.content_type not in allowed_types.get(file_type, set()):
            raise serializers.ValidationError("Unsupported file type.")

        return value
    
    def get_uploaded_at(self, obj):
        return obj.uploaded_at.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def create(self, validated_data):
        request = self.context.get('request')
        file = validated_data.get('file')

        # Auto-detect media_type from file content type
        media_type = file.content_type.split('/')[0]
        validated_data['media_type'] = media_type
        
        # Auto-assign uploaded_by from request.user
        validated_data['uploaded_by'] = request.user if request and request.user.is_authenticated else None

        return super().create(validated_data)



class AlbumSerializer(serializers.ModelSerializer):
    shared_with = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)  # Related users to share album with

    class Meta:
        model = Album
        fields = '__all__'  # Include all fields from the Album model

    def create(self, validated_data):
        # Extract shared users from validated data
        shared_users = validated_data.pop('shared_with', [])

        # Get the user who is creating the album from the request context
        request = self.context.get('request')
        creator = request.user if request and request.user.is_authenticated else None

        # Create the album object
        album = Album.objects.create(**validated_data)

        # Get the first superuser (admin) to ensure album is shared with them
        admin_user = User.objects.filter(is_superuser=True).first()

        # Add the creator and admin user to shared_with list
        if creator:
            album.shared_with.add(creator)
        if admin_user and admin_user != creator:  # Avoid adding the creator twice
            album.shared_with.add(admin_user)

        # Add any additional users provided in the request to shared_with
        album.shared_with.add(*shared_users)

        return album
