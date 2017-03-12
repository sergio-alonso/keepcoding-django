"""Django blog app tests."""
from blog.views import home_page
from django.core.urlresolvers import resolve
from django.test import TestCase


class HomePageTest(TestCase):
    """Home page test cases."""

    def test_root_url_resolves_to_home_page_view(self):
        """Test case: root url resolves to home page view.

        Check that resolve, when called with the root of the site finds a function called home_page.
        """
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """Test case: home page returns correct HTML.

        A function that returns real response with HTML to the browser.
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
