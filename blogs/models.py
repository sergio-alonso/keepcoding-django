from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

class Post(models.Model):
    """Post model."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.TextField(default='', unique=True)
    summary = models.TextField(default='', null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    imagen = models.URLField(default='', null=True, blank=True)
    category = TaggableManager(blank=True)
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """__str___."""
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.owner.email, self.id])

    def get_author(self):
        return self.owner
