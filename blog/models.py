"""Django blog app models."""
from django.db import models
from django.core.urlresolvers import reverse


class Blog(models.Model):
    """Blog model."""

    def get_absolute_url(self):
        """Say what page displays the item."""
        return reverse('list-posts', args=[self.id])

    pass


class Post(models.Model):
    """Post model."""

    title = models.TextField(default='')
    blog = models.ForeignKey(Blog, default=None)
