"""Django blog app models."""
from django.db import models


class Post(models.Model):
    """Post model."""

    title = models.TextField(default='')
