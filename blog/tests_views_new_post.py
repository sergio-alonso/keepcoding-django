"""Django blog app tests."""
from django.core.urlresolvers import resolve
from django.test import TestCase

from blog.models import Post
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

    def test_can_save_a_POST_request(self):
        """Test case: save a POST request.

        A function that saves a post request.
        """
        self.client.post('/new-post/', data={'post-title': 'A new blog post'})

        self.assertEqual(Post.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.title, 'A new blog post')

    def test_redirects_after_a_POST(self):
        """Test case: redirects after a POST."""
        response = self.client.post('/new-post/', data={'post-title': 'A new blog post'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), '/new-post/')

    def test_only_save_posts_when_necessary(self):
        """Test case: only save posts when necessary."""
        self.client.get('/new-post/')
        self.assertEqual(Post.objects.count(), 0)
