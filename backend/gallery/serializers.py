from rest_framework import serializers
from gallery.models import Album, Media
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# TODO: CHECK SOME TUTORIALS ON HOW DJANGO REST FRAMEWORK WORKS, BECAUSE I AM NOT SURE IF THIS IS THE RIGHT WAY TO DO IT
# USERSERUIALIZER should work in views when listing, but it didn't change the model's meta in the db itself
# SHOULD WORK WITH gallery_album_shared_with table that connects user and album, have no clue how to implement it though


# class AlbumSerializer(serializers.ModelSerializer):
#     shared_with = UserSerializer(many=True, read_only=True)

#     class Meta:
#         model = Album
#         fields = '__all__'

def validate_file(value):
    allowed_types = ['image/jpeg', 'image/png', 'video/mp4', 'audio/mpeg']
    
    if hasattr(value, 'content_type') and value.content_type not in allowed_types:
        raise serializers.ValidationError("Unsupported file type.")
    
    return value

class MediaSerializer(serializers.ModelSerializer):
    file = serializers.FileField(validators=[validate_file])

    class Meta:
        model = Media
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    shared_with = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = Album
        fields = '__all__'

    def create(self, validated_data):
        # Extract shared users from validated data
        shared_users = validated_data.pop('shared_with', [])

        # Get the user who is creating the album
        request = self.context.get('request')
        creator = request.user if request and request.user.is_authenticated else None

        # Create the album
        album = Album.objects.create(**validated_data)

        # Get the admin user
        admin_user = User.objects.filter(is_superuser=True).first()

        # Ensure the creator and admin are added to shared_with
        if creator:
            album.shared_with.add(creator)
        if admin_user and admin_user != creator:  # Avoid duplicates
            album.shared_with.add(admin_user)

        # Add any additional users provided in the request
        album.shared_with.add(*shared_users)

        return album