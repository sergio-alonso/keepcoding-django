"""Django accounts models."""

from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.urlresolvers import reverse

import uuid
import re

auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class UserManager(auth.models.BaseUserManager):
    """User Manager."""

    def create_user(self, email, password=None, is_admin=False):
        """Create user."""

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            password = password
        )

        user.is_admin = is_admin

        if password == None:
            user.password = 'supersecret'

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create superuser."""
        self.create_user(email, password, is_admin=True)

class User(models.Model):
    """User model."""

    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=50)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    is_anonymous = False
    is_authenticated = True

    def get_username(self):
        # The user is identified by their email address
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def check_password(self, password):
        return self.password == password

    def set_password(self, password):
        self.password = password

    def get_absolute_url(self):
        return reverse('api:user-detail', args=[self.email])

    def get_blog_url(self):
        return reverse('api:blogs-detail', args=[self.email])

class Token(models.Model):
    """Token model."""

    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)
