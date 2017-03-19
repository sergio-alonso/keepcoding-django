"""Blogs views tests."""
from django.http import HttpRequest
from django.test import TestCase

import unittest
from unittest.mock import patch, Mock

from blogs.forms import PostForm
from blogs.views import post_save

class HomeViewTest(TestCase):
    """Test suite: home view."""

    def test_uses_home_template(self):
        """Test case: uses home template."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class BlogViewTest(TestCase):
    """Test suite: blog view."""

    def test_uses_blog_template(self):
        """Test case: uses blog template."""
        response = self.client.get('/blogs/user.name@example.com/')
        self.assertTemplateUsed(response, 'blog.html')

class NewPostViewTest(TestCase):
    """Test suite: new post view."""

    def test_uses_post_template(self):
        """Test case: uses post template."""
        response = self.client.get('/new-post')
        self.assertTemplateUsed(response, 'post_create.html')

    def test_uses_post_form(self):
        """Test case: uses post form."""
        response = self.client.get('/new-post')
        self.assertIsInstance(response.context['form'], PostForm)


@patch('blogs.views.NewPostForm')
class NewPostViewUnitTest(unittest.TestCase):
    """Test suite: new post view unit test."""

    def setUp(self):
        """"Setup."""
        self.request = HttpRequest()
        self.request.POST['title'] = "New post"
        self.request.user = Mock()
        self.request.user.email = "user.name@example.com"

    def test_passes_POST_data_to_create_post_form(self, mockNewPostForm):
        """Test case: passes POST data to create post form."""
        post_save(self.request)
        mockNewPostForm.assert_called_once_with(data=self.request.POST)

    @patch('blogs.views.redirect')
    def test_redirect_to_blog_if_form_is_valid(self, mock_redirect, mockNewPostForm):
        """Test case: redirect to blog if form is valid."""
        mock_form = mockNewPostForm.return_value
        mock_form.is_valid.return_value = True

        response = post_save(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with('blog', user_email=self.request.user.email)

    @patch('blogs.views.render')
    def test_renders_post_create_form_if_form_is_invalid(self, mock_render, mockNewPostForm):
        """Test case: renders post create form if form is invalid."""
        mock_form = mockNewPostForm.return_value
        mock_form.is_valid.return_value = False

        response = post_save(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(self.request, 'post_create.html', {'form': mock_form})

    def test_does_not_save_if_form_invalid(self, mockNewBlogForm):
        """Test case: does not save if form invalid."""
        mock_form = mockNewBlogForm.return_value
        mock_form.is_valid.return_value = False

        post_save(self.request)

        self.assertFalse(mock_form.save.called)
