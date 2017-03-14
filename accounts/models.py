"""Django accounts models."""

from django.contrib import auth
from django.db import models

import uuid

auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    """User model."""

    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    """Token model."""

    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)


# class ListUserManager(auth.BaseUserManager):
#     """List User Manager."""

#     def create_user(self, email):
#         """Create user."""
#         ListUser.objects.create(email=email)

#     def create_superuser(self, email, password):
#         """Create superuser."""
#         self.create_user(email)


# class ListUser(auth.AbstractBaseUser, auth.PermissionsMixin):
#     """List User."""

#     email = models.EmailField(primary_key=True)
#     USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['email', 'height']
#     objects = ListUserManager()

#     @property
#     def is_staff(self):
#         """Check if is staff."""
#         return self.email == 'admin@example.com'

#     @property
#     def is_active(self):
#         """Check if is active."""
#         return True
