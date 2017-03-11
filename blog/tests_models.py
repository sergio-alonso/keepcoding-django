"""Django blog models tests."""
from django.test import TestCase

from blog.models import Post


class PostModelTest(TestCase):
    """Post model test cases."""

    def test_saving_and_retrieving_posts(self):
        """Test case: sva and retireve posts."""
        first_post = Post()
        first_post.title = 'A first post'
        first_post.save()

        second_post = Post()
        second_post.title = 'A second post'
        second_post.save()

        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 2)

        first_saved_item = saved_posts[0]
        second_saved_item = saved_posts[1]

        self.assertEqual(first_saved_item.title, 'A first post')
        self.assertEqual(second_saved_item.title, 'A second post')
