"""Blogs views tests."""
from django.http import HttpRequest
from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()

import unittest
from unittest.mock import patch, Mock

from django_seed import Seed

from blogs.forms import PostForm
from blogs.views import post_save
from blogs.models import Post

class HomeViewTest(TestCase):
    """Test suite: home view."""

    def test_uses_home_template(self):
        """Test case: uses home template."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_displays_last_post(self):
        """Test case: displays last posts."""

        seeder = Seed.seeder()
        seeder.add_entity(User, 10)
        seeder.add_entity(Post, 10)
        seeder.execute()

        response = self.client.get('/')
        post_list = response.context["object_list"]

        # Test if posts are sorted by date, from newest to oldest
        assert(all(a.published_date >= b.published_date for a, b in zip(post_list, post_list[1:])))

    @unittest.skip
    def test_display_only_ten_posts(self):
        self.fail("Finish the test!")

    @unittest.skip
    def test_pagination(self):
        self.fail("Finish the test!")

class BlogViewTest(TestCase):
    """Test suite: blog view."""

    def test_uses_blog_template(self):
        """Test case: uses blog template."""
        user = User.objects.create(email="user.name@example.com")
        response = self.client.get('/blogs/%s/' % user.email)
        self.assertTemplateUsed(response, 'blog.html')

    def test_passes_correct_owner_to_template(self):
        """Test case: passes correct owner to template."""
        User.objects.create(email='wrong.user@example.com')
        correct_user = User.objects.create(email='user.name@example.com')
        response = self.client.get('/blogs/%s/' % correct_user.email)
        self.assertEqual(response.context['owner'], correct_user)

    def test_displays_only_post_for_that_user(self):
        """Test case: displays only post for that user."""
        correct_user = User.objects.create(email='user.name@example.com')
        Post.objects.create(title='post 0', owner=correct_user)
        Post.objects.create(title='post 1', owner=correct_user)
        other_user = User.objects.create(email='wrong.user@example.com')
        Post.objects.create(title='other user post 0', owner=other_user)
        Post.objects.create(title='other user post 1', owner=other_user)

        response = self.client.get('/blogs/%s/' % correct_user.email)

        self.assertContains(response, 'post 0')
        self.assertContains(response, 'post 1')
        self.assertNotContains(response, 'other user post 0')
        self.assertNotContains(response, 'other user post 1')

    def test_displays_posts_sorted_by_publication_date(self):
        """Test case: displays last posts."""

        seeder = Seed.seeder()
        seeder.add_entity(User, 1)
        seeder.add_entity(Post, 10)
        seeder.execute()

        response = self.client.get('/blogs/%s/' % User.objects.all()[:1].get().email)
        post_list = response.context["posts"]

        # Test if posts are sorted by date, from newest to oldest
        assert(all(a.published_date >= b.published_date for a, b in zip(post_list, post_list[1:])))


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
