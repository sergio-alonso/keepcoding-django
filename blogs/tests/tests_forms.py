"""Blog forms tests."""
from django.test import TestCase

import unittest
from unittest.mock import patch, Mock

from blogs.forms import PostForm, NewPostForm,  EMPTY_POST_TITLE_ERROR, DUPLICATE_POST_TITLE_ERROR
from blogs.models import Post


class PostFormTest(TestCase):
    """Test suite: post form tests."""

    def test_form_title_input_has_placeholder_and_css_classes(self):
        """Test case: form title input has placeholder and css classes."""
        form = PostForm()
        self.assertIn('placeholder="Enter a post title"', form.as_p())
        self.assertIn('class="post-title"', form.as_p())


    def test_form_validation_for_blank_posts(self):
        """Test case: form validation for blank items."""
        form = PostForm(data={'title': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], [EMPTY_POST_TITLE_ERROR])

    def test_form_validation_for_duplicate_posts(self):
        """Test case: form validation forn duplicate items."""
        Post.objects.create(title='no twins!')
        form = PostForm(data={'title': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], [DUPLICATE_POST_TITLE_ERROR])


class NewPostFormTest(unittest.TestCase):
    """Test suite: new post form tests."""

    @patch('blogs.forms.Post.objects.create')
    def test_avoid_create_post_if_user_is_not_authenticated(self, mock_Post_objects_create):
        """Test case: avoid create post if user is not authenticated."""
        user = Mock(is_authenticated=False)
        form = NewPostForm(data={'title': 'new post title'})
        form.is_valid()
        form.save(owner=user)
        mock_Post_objects_create.assert_not_called()

    @patch('blogs.forms.Post.objects.create')
    def test_save_creates_new_post_with_owner_if_user_is_authenticated(self, mock_Post_objects_create):
        """Test case: save creates new post with owner if user is authenticated."""
        user = Mock(is_authenticated=True)
        form = NewPostForm(data={'title': 'new post title'})
        form.is_valid()
        form.save(owner=user)
        mock_Post_objects_create.assert_called_once_with(
            title='new post title', owner=user
        )

    @patch('blogs.forms.Post.objects.create')
    def test_save_returns_new_post_object(self, mock_Post_objects_create):
        """Test case: save return new post object."""
        user = Mock(is_authenticated=True)
        form = NewPostForm(data={'title': 'new post title'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_Post_objects_create.return_value)
