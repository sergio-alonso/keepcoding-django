"""Django accounts authentication."""
from accounts.models import Token, User


class PasswordlessAuthenticationBackend(object):
    """Passwordless Authentication Backend."""

    def authenticate(self, uid):
        """Authenticate."""
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        """Get user."""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
