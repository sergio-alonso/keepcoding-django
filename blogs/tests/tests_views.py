"""Blogs views tests."""
from django.test import TestCase


class HomeViewTest(TestCase):
    """Test suite: home view."""

    def test_uses_home_template(self):
        """Test case: uses home template."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
