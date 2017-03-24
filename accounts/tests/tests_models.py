"""Django accounts tests."""
from django.test import TestCase
from django.contrib import auth
from accounts.models import Token

User = auth.get_user_model()


class UserModelTest(TestCase):
    """Test suite: user models."""

    def test_email_is_primary_key(self):
        """Test case: email is primary key."""
        user = User()
        self.assertFalse(hasattr(user, 'id'))

    def test_user_is_valid_with_email_only(self):
        """Test case: user is valid with email."""
        user = User(email='user.name@example.com', password="supersecret")
        user.full_clean()  # should not raise

    def test_no_problem_with_auth_login(self):
        """Test case: no problem with auth login."""
        user = User.objects.create(email='user.name@example.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)  # should not raise


class TokenModelTest(TestCase):
    """Test suite: token model."""

    def test_links_user_with_auto_generated_uid(self):
        """Test case: link user with auto generated uid."""
        token1 = Token.objects.create(email='user.name@example.com')
        token2 = Token.objects.create(email='user.name@example.com')
        self.assertNotEqual(token1.uid, token2.uid)
