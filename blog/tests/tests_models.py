"""Django blog models tests."""
from django.test import TestCase
from django.core.exceptions import ValidationError

from blog.models import Blog, Post


class PostModelTest(TestCase):
    """Test suite: post model test cases."""

    def test_saving_and_retrieving_posts(self):
        """Test case: sva and retireve posts."""
        blog = Blog()
        blog.save()

        first_post = Post()
        first_post.title = 'A first post'
        first_post.blog = blog
        first_post.save()

        second_post = Post()
        second_post.title = 'A second post'
        second_post.blog = blog
        second_post.save()

        saved_blog = Blog.objects.first()
        self.assertEqual(saved_blog, blog)

        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 2)

        first_saved_item = saved_posts[0]
        second_saved_item = saved_posts[1]

        self.assertEqual(first_saved_item.title, 'A first post')
        self.assertEqual(first_saved_item.blog, blog)
        self.assertEqual(second_saved_item.title, 'A second post')
        self.assertEqual(second_saved_item.blog, blog)

    def test_cannot_create_empty_blog_posts(self):
        """Test case: cannot create empty blog posts."""
        blog = Blog.objects.create()
        post = Post(blog=blog, title='')
        with self.assertRaises(ValidationError):
            post.save()
            post.full_clean()

    def test_get_absolute_url(self):
        """Test case: get absolute url."""
        blog = Blog.objects.create()
        self.assertEqual(blog.get_absolute_url(), '/blog/%d/' % (blog.id))
