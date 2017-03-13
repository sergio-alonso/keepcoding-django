"""Django blog view tests."""
from django.test import TestCase
from django.utils.html import escape

from blog.forms import PostForm
from blog.models import Blog, Post


class HomeViewTest(TestCase):
    """Home test cases."""

    def test_home_page_returns_correct_html(self):
        """Test case: home page returns correct HTML."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_posts_form(self):
        """Test case: home page uses posts form."""
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], PostForm)


class NewBlogViewTest(TestCase):
    """New blog page test cases."""

    def test_can_save_a_POST_request(self):
        """Test case: can save a POST request."""
        self.client.post('/blog/new', data={'post-title': 'A new blog post'})

        self.assertEqual(Post.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.title, 'A new blog post')

    def test_redirects_after_a_POST(self):
        """Test case: redirects after a POST."""
        response = self.client.post('/blog/new', data={'post-title': 'A new blog post'})
        new_blog = Blog.objects.first()
        self.assertRedirects(response, '/blog/%d/' % (new_blog.id))

    def test_validation_errors_are_sent_back_to_home_template(self):
        """Test case: validation errors are sent back to home template."""
        response = self.client.post('/blog/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        """Test case: invalid list items arent saved."""
        self.client.post('/blog/new', data={'post-title': ''})
        self.assertEqual(Blog.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)


class ListPostViewTest(TestCase):
    """List post view test cases."""

    def test_uses_list_post_template(self):
        """Test case: use list post template."""
        blog = Blog.objects.create()
        response = self.client.get('/blog/%d/' % (blog.id,))
        self.assertTemplateUsed(response, 'list-posts.html')

    def test_passes_correct_blog_to_template(self):
        """Test case: passes correct blog to template."""
        another_blog = Blog.objects.create()
        correct_blog = Blog.objects.create()
        response = self.client.get('/blog/%d/' % (correct_blog.id,))
        self.assertEqual(response.context['blog'], correct_blog)
        self.assertNotEqual(response.context['blog'], another_blog)

    def test_displays_only_posts_for_that_blog(self):
        """Test case: display all post items for a blog."""
        correct_blog = Blog.objects.create()
        Post.objects.create(title='blog post 0', blog=correct_blog)
        Post.objects.create(title='blog post 1', blog=correct_blog)

        another_blog = Blog.objects.create()
        Post.objects.create(title='another blog post 0', blog=another_blog)
        Post.objects.create(title='another blog post 1', blog=another_blog)

        response = self.client.get('/blog/%d/' % (correct_blog.id,))

        self.assertContains(response, 'blog post 0')
        self.assertContains(response, 'blog post 1')
        self.assertNotContains(response, 'another blog post 0')
        self.assertNotContains(response, 'another blog post 1')

    def test_can_save_a_POST_request_to_an_existing_blog(self):
        """Test case: can save a post request to an existing blog."""
        another_blog = Blog.objects.create()
        correct_blog = Blog.objects.create()

        self.client.post(
            '/blog/%d/' % (correct_blog.id,),
            data={'post-title': 'A new post for an existing blog'}
        )

        self.assertEqual(Post.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.title, 'A new post for an existing blog')
        self.assertEqual(new_post.blog, correct_blog)
        self.assertNotEqual(new_post.blog, another_blog)

    def test_POST_redirects_to_blog_view(self):
        """Test case: redirects to blog view."""
        another_blog = Blog.objects.create()
        correct_blog = Blog.objects.create()

        response = self.client.post(
            '/blog/%d/' % (correct_blog.id,),
            data={'post-title': 'A new post for an existing blog'}
        )

        self.assertNotEqual(correct_blog.id, another_blog.id)
        self.assertRedirects(response, '/blog/%d/' % (correct_blog.id,))

    def test_validation_errors_end_up_on_lists_page(self):
        """Test case: validation errors end up on posts page."""
        blog = Blog.objects.create()
        response = self.client.post(
            '/blog/%d/' % (blog.id),
            data={'post-title': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list-posts.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
