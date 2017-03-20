"""Blog models tests."""

from django.test import TestCase
from django.core.exceptions import ValidationError
from blogs.models import Post
from django.contrib.auth import get_user_model
User = get_user_model()

class PostModelTest(TestCase):

    def test_default_title(self):
        """Test case: default title."""
        post = Post()
        self.assertEqual(post.title, '')

    def test_cannot_save_empty_list_posts(self):
        """Test case: cannot save empty list post."""
        post = Post(title='')
        with self.assertRaises(ValidationError):
            post.save()
            post.full_clean()

    def test_duplicate_posts_are_invalid(self):
        """Test case: duplicate post are invalid."""
        Post.objects.create(title='post title')
        with self.assertRaises(ValidationError):
            post = Post(title='post title')
            post.full_clean()

    def test_string_representation(self):
        """Test case: string representation."""
        post = Post(title='post title')
        self.assertEqual(str(post), 'post title')

    def test_post_can_have_owners(self):
        Post(owner=User())

    def test_list_owner_is_not_optional(self):
        with self.assertRaises(ValidationError):
            Post().full_clean()
