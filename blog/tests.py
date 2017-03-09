"""Django blog app tests."""
from django.test import TestCase


class SmokeTest(TestCase):
    """A deliberately silly failing tests."""

    def test_bad_maths(self):
        """Fail."""
        self.assertEqual(1 + 1, 3)
