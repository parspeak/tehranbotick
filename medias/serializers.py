from rest_framework import serializers
from medias.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'alt_text', 'image', 'created_by', 'last_modified_by', 'created_at', 'last_modified')
        read_only_fields = ('id', 'created_by', 'last_modified_by', 'created_at', 'last_modified')
