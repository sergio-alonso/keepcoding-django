from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

class Category(models.Model):

    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Post model."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.TextField(default='', unique=True)
    summary = models.TextField(default='', null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    imagen = models.URLField(default='', null=True, blank=True)
    category = models.ManyToManyField(Category)
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """__str___."""
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.owner.email, self.id])
