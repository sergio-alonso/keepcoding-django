from rest_framework import serializers
from uploader.models import Image

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'
