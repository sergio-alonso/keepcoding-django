"""Django blog app tests."""
from django.test import TestCase

from blog.models import Post


class ListPostViewTest(TestCase):
    """List post view test cases."""

    def test_uses_list_blog_template(self):
        """Test case: use list post template."""
        response = self.client.get('/blog/the-only-blog-in-the-world/')
        self.assertTemplateUsed(response, 'list-posts.html')

    def test_displays_all_post_items(self):
        """Test case: display all post items."""
        Post.objects.create(title='blog post 0')
        Post.objects.create(title='blog post 1')

        response = self.client.get('/blog/the-only-blog-in-the-world/')

        self.assertContains(response, 'blog post 0')
        self.assertContains(response, 'blog post 1')
