"""Django blog models."""
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class Blog(models.Model):
    """Blog model."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self):
        """Say what page displays the item."""
        return reverse('list-posts', args=[self.id])

    @staticmethod
    def create_new(first_post_title, owner=None):
        """Create new."""
        blog = Blog.objects.create(owner=owner)
        Post.objects.create(title=first_post_title, blog=blog)
        return blog

    @property
    def name(self):
        return self.post_set.first().title


class Post(models.Model):
    """Post model."""

    title = models.TextField(default='')
    blog = models.ForeignKey(Blog, default=None)
