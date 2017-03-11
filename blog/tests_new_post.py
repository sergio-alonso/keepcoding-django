"""Django blog app tests."""
from django.core.urlresolvers import resolve
from django.test import TestCase

from blog.views import new_post_page


class NewPostPageTest(TestCase):
    """New post page test cases."""

    def test_url_resolves_to_new_post_page_view(self):
        """Test case: url resolves to new post page view.

        Check that resolve, when called with the url of the new post finds a function called new_post_page.
        """
        found = resolve('/new-post/')
        self.assertEqual(found.func, new_post_page)

    def test_new_post_page_returns_correct_html(self):
        """Test case: page returns correct HTML.

        A function that returns real response with HTML to the browser.
        """
        response = self.client.get('/new-post/')
        self.assertTemplateUsed(response, 'new-post.html')
