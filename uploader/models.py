from django.db import models
from django.conf import settings


class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    file = models.FileField(upload_to=settings.MEDIA_ROOT)
