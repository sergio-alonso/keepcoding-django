"""Django blog view tests."""
from django.test import TestCase
from django.utils.html import escape
from django.contrib.auth import get_user_model

from blog.forms import PostForm, EMPTY_POST_TITLE_ERROR
from blog.models import Blog, Post
from blog.views import new_blog

import unittest
from unittest.mock import patch, Mock
from django.http import HttpRequest

User = get_user_model()


class HomeViewTest(TestCase):
    """Home view test suite."""

    def test_uses_home_template(self):
        """Test case: home page returns correct HTML."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_uses_posts_form(self):
        """Test case: home page uses posts form."""
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], PostForm)


@patch('blog.views.NewBlogForm')
class NewBlogViewUnitTest(unittest.TestCase):
    """New blog view unit test."""

    def setUp(self):
        """"Setup."""
        self.request = HttpRequest()
        self.request.POST['title'] = "New blog post"
        self.request.user = Mock()

    def test_passes_POST_data_to_NewBlogFrom(self, mockNewBlogForm):
        """Test case: passes POST data to NewBlogForm."""
        new_blog(self.request)
        mockNewBlogForm.assert_called_once_with(data=self.request.POST)

    @patch('blog.views.redirect')
    def test_redirects_to_form_with_owner_if_form_valid(self, mock_redirect, mockNewBlogForm):
        """Test cas: redirects to form with owner if form valid."""
        mock_form = mockNewBlogForm.return_value
        mock_form.is_valid.return_value = True

        response = new_blog(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('blog.views.render')
    def test_renders_home_template_with_form_if_form_is_invalid(self, mock_render, mockNewBlogForm):
        """Test case: renders home template with form if form is invalid."""
        mock_form = mockNewBlogForm.return_value
        mock_form.is_valid.return_value = False

        response = new_blog(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(self.request, 'home.html', {'form': mock_form})

    def test_does_not_save_if_form_invalid(self, mockNewBlogForm):
        """Test case: does not save if form invalid."""
        mock_form = mockNewBlogForm.return_value
        mock_form.is_valid.return_value = False

        new_blog(self.request)

        self.assertFalse(mock_form.save.called)


class NewBlogViewIntegratedTest(TestCase):
    """New blog view test cases."""

    def test_can_save_a_POST_request(self):
        """Test case: can save a POST request."""
        self.client.post('/blog/new', data={'title': 'A new blog post'})

        self.assertEqual(Post.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.title, 'A new blog post')

    def test_redirects_after_a_POST(self):
        """Test case: redirects after a POST."""
        response = self.client.post('/blog/new', data={'title': 'A new blog post'})
        new_blog = Blog.objects.first()
        self.assertRedirects(response, '/blog/%d/' % (new_blog.id))

    def test_invalid_blog_posts_arent_saved(self):
        """Test case: invalid list items arent saved."""
        self.client.post('/blog/new', data={'title': ''})
        self.assertEqual(Blog.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self):
        """Test case: for invalid input renders home template."""
        response = self.client.post('/blog/new', data={'title': str()})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        """Test case: validation errors are shown on home page."""
        response = self.client.post('/blog/new', data={'title': ''})
        self.assertContains(response, escape(EMPTY_POST_TITLE_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        """Test case: forinvalid input passes form to template."""
        response = self.client.post('/blog/new', data={'title': ''})
        self.assertIsInstance(response.context['form'], PostForm)

    def test_blog_owner_is_saved_if_user_is_authenticated(self):
        """Test case: blog owner is saved if user is authenticated."""
        user = User.objects.create(email='user.name@example.com')
        self.client.force_login(user)
        self.client.post('/blog/new', data={'title': 'new post'})
        blog = Blog.objects.first()
        self.assertEqual(blog.owner, user)


class ListPostViewTest(TestCase):
    """List post view test cases."""

    def test_uses_list_template(self):
        """Test case: use list posts template."""
        blog = Blog.objects.create()
        response = self.client.get('/blog/%d/' % blog.id)
        self.assertTemplateUsed(response, 'list-posts.html')

    def test_displays_post_form(self):
        """Test case: display post form."""
        blog = Blog.objects.create()
        response = self.client.get('/blog/%d/' % (blog.id))
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertContains(response, 'name="title"')

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

    @unittest.skip
    def test_can_save_a_POST_request_to_an_existing_blog(self):
        """Test case: can save a post request to an existing blog."""
        another_blog = Blog.objects.create()
        correct_blog = Blog.objects.create()

        self.client.post(
            '/blog/%d/' % (correct_blog.id,),
            data={'title': 'A new post for an existing blog'}
        )

        self.assertEqual(Post.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.title, 'A new post for an existing blog')
        self.assertEqual(new_post.blog, correct_blog)
        self.assertNotEqual(new_post.blog, another_blog)

    @unittest.skip
    def test_POST_redirects_to_blog_view(self):
        """Test case: redirects to blog view."""
        another_blog = Blog.objects.create()
        correct_blog = Blog.objects.create()

        response = self.client.post(
            '/blog/%d/' % (correct_blog.id,),
            data={'title': 'A new post for an existing blog'}
        )

        self.assertNotEqual(correct_blog.id, another_blog.id)
        self.assertRedirects(response, '/blog/%d/' % (correct_blog.id,))

    def post_invalid_input(self):
        """Post invalid input."""
        blog = Blog.objects.create()
        return self.client.post(
            '/blog/%d/' % (blog.id,),
            data={'title': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        """Test case: for invalid input nothing saved to db."""
        self.post_invalid_input()
        self.assertEqual(Post.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        """Test case: use list post template."""
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list-posts.html')

    def test_for_invalid_input_passes_form_to_template(self):
        """Test case: for invalid input passes form to template."""
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], PostForm)

    def test_for_invalid_input_shows_error_on_page(self):
        """Test case: for invalid input shows error on page."""
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_POST_TITLE_ERROR))


class MyBlogTest(TestCase):
    """My blog test suite."""

    def test_my_blog_url_renders_my_blog_template(self):
        """Test case: my blog url renders my blog template."""
        User.objects.create(email='user.name@example.com')
        response = self.client.get('/blog/users/user.name@example.com/')
        self.assertTemplateUsed(response, 'my_blog.html')
