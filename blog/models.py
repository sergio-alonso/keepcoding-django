"""Django blog app models."""
from django.db import models


class Blog(models.Model):
    """Blog model."""

    pass


class Post(models.Model):
    """Post model."""

    title = models.TextField(default='')
    blog = models.ForeignKey(Blog, default=None)
