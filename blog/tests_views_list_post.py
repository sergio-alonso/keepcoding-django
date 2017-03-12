"""Django blog app tests."""
from django.test import TestCase

from blog.models import Blog, Post


class ListPostViewTest(TestCase):
    """List post view test cases."""

    def test_uses_list_blog_template(self):
        """Test case: use list post template."""
        blog = Blog.objects.create()
        response = self.client.get('/blog/%d/' % (blog.id,))
        self.assertTemplateUsed(response, 'list-posts.html')

    def test_displays_only_items_for_that_blog(self):
        """Test case: display all post items for a blog."""
        own_blog = Blog.objects.create()
        Post.objects.create(title='blog post 0', blog=own_blog)
        Post.objects.create(title='blog post 1', blog=own_blog)

        other_blog = Blog.objects.create()
        Post.objects.create(title='other blog post 0', blog=other_blog)
        Post.objects.create(title='other blog post 1', blog=other_blog)

        response = self.client.get('/blog/%d/' % (own_blog.id,))

        self.assertContains(response, 'blog post 0')
        self.assertContains(response, 'blog post 1')
        self.assertNotContains(response, 'other blog post 0')
        self.assertNotContains(response, 'other blog post 1')

    def test_passes_correct_blog_to_template(self):
        """Test case: passes correct blog to template."""
        Blog.objects.create()  # Create another blog
        correct_blog = Blog.objects.create()
        response = self.client.get('/blog/%d/' % (correct_blog.id,))
        self.assertEqual(response.context['blog'], correct_blog)
