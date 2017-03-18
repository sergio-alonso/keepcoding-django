"""Django blog test forms."""
import unittest
from unittest.mock import patch, Mock

from django.test import TestCase

from blog.forms import PostForm, NewBlogForm, EMPTY_POST_TITLE_ERROR
from blog.models import Blog, Post


class PostFormTest(TestCase):
    """Test suite: post form test."""

    def test_form_post_input_has_placeholder_and_css_classes(self):
        """Test case: form renders post title input."""
        form = PostForm()
        self.assertIn('placeholder="Enter a post title"', form.as_p())
        self.assertIn('class="post-title"', form.as_p())

    def test_form_validation_for_blank_posts(self):
        """Test case: form validation for blank posts."""
        form = PostForm(data={'title': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['title'], [EMPTY_POST_TITLE_ERROR]
        )


class NewBlogFormTest(unittest.TestCase):
    """Test suite: New blog form test."""

    @patch('blog.forms.Blog.create_new')
    def test_save_creates_new_blog_from_post_data_if_user_is_not_authenticated(self, mock_Blog_create_new):
        """Test case: save creates new blog from post data if user is not authenticated."""
        user = Mock(is_authenticated=False)
        form = NewBlogForm(data={'title': 'New post title'})
        form.is_valid()
        form.save(owner=user)
        mock_Blog_create_new.assert_called_once_with(first_post_title='New post title')

    @patch('blog.forms.Blog.create_new')
    def test_save_creates_new_blog_with_owner_if_user_authenticated(self, mock_Blog_create_new):
        """Test case: save creates new blog with owner if user authenticated."""
        user = Mock(is_authenticated=True)
        form = NewBlogForm(data={'title': 'New post title'})

        form.is_valid()
        form.save(owner=user)

        mock_Blog_create_new.assert_called_once_with(first_post_title='New post title', owner=user)

    @patch('blog.forms.Blog.create_new')
    def test_save_returns_new_blog_object(self, mock_Blog_create_new):
        """Test case: save returns new blog object."""
        user = Mock(is_authenticated=True)
        form = NewBlogForm(data={'title': 'New post title'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_Blog_create_new.return_value)
