"""Django accounts authentication tests."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()


class AuthenticateTest(TestCase):
    """Tests suite: authenticate."""

    def test_returns_None_if_no_such_token(self):
        """Test case: returns none if no such token."""
        result = PasswordlessAuthenticationBackend().authenticate(
            'no-such-token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        """Test case: returns new user with correct email if token exists."""
        email = 'user.name@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        """Test case: returns existing user with correct email if tocken exists."""
        email = 'user.name@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)

    def test_gets_user_by_email(self):
        """Test case: get user by email."""
        User.objects.create(email='user.name.1@example.com')
        desired_user = User.objects.create(email='user.name.0@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user(
            'user.name.0@example.com'
        )
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        """Test case: return none if no user with that email."""
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('user.name@example.com')
        )
