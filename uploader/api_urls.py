from rest_framework import routers

from .viewsets import UploadViewSet

router = routers.SimpleRouter()
router.register(r'upload', UploadViewSet)
