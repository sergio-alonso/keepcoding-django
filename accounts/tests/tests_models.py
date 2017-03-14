"""Django accounts tests."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Token

User = get_user_model()


class UserModelTest(TestCase):
    """Test suite: user models."""

    def test_email_is_primary_key(self):
        """Test case: email is primary key."""
        user = User()
        self.assertFalse(hasattr(user, 'id'))

    def test_user_is_valid_with_email_only(self):
        """Test case: user is valid with email."""
        user = User(email='user.name@example.com')
        user.full_clean()  # should not raise


class TokenModelTest(TestCase):
    """Test suite: token model."""

    def test_links_user_with_auto_generated_uid(self):
        """Test case: link user with auto generated uid."""
        token1 = Token.objects.create(email='user.name@example.com')
        token2 = Token.objects.create(email='user.name@example.com')
        self.assertNotEqual(token1.uid, token2.uid)
