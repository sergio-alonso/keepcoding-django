"""Django accounts models."""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Token(models.Model):
    """Token model."""

    email = models.EmailField()
    uid = models.CharField(max_length=255)


class ListUserManager(BaseUserManager):
    """List User Manager."""

    def create_user(self, email):
        """Create user."""
        ListUser.objects.create(email=email)

    def create_superuser(self, email, password):
        """Create superuser."""
        self.create_user(email)


class ListUser(AbstractBaseUser, PermissionsMixin):
    """List User."""

    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email', 'height']

    objects = ListUserManager()

    @property
    def is_staff(self):
        """Check if is staff."""
        return self.email == 'admin@example.com'

    @property
    def is_active(self):
        """Check if is active."""
        return True
