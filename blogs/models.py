from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

class Post(models.Model):
    """Post model."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.TextField(default='', unique=True)
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """__str___."""
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.owner.email, self.id])
