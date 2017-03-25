from rest_framework import viewsets

from uploader.models import Image
from uploader.serializers import ImageSerializer

class UploadViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
