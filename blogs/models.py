from django.conf import settings
from django.db import models


class Post(models.Model):
    """Post model."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.TextField(default='', unique=True)

    def __str__(self):
        """__str___."""
        return self.title
