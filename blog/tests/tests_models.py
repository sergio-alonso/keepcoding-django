"""Django blog models tests."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from blog.models import Blog, Post

User = get_user_model()

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

    def test_create_new_creates_blog_and_first_post(self):
        """Test case: create new creates blog and first post."""
        Blog.create_new(first_post_title='New post title')
        new_post = Post.objects.first()
        self.assertEqual(new_post.title, 'New post title')
        new_blog = Blog.objects.first()
        self.assertEqual(new_post.blog, new_blog)

    def test_create_new_optionally_saves_owner(self):
        """Test case: create new optionally saves owner."""
        user = User.objects.create()
        Blog.create_new(first_post_title='New item text', owner=user)
        new_blog = Blog.objects.first()
        self.assertEqual(new_blog.owner, user)


class BlogModelTest(TestCase):
    """Test suite: Blog model test.."""

    def test_blog_can_have_owners(self):
        """Test case: blog can have owners."""
        Blog(owner=User())  # should not raise

    def test_blog_owner_is_optional(self):
        """Test case: blog owner is optional."""
        Blog().full_clean()  # should not raise

    def test_create_returns_new_blog_object(self):
        """Test case: create returns new blog object."""
        returned = Blog.create_new(first_post_title='New post title')
        new_blog = Blog.objects.first()
        self.assertEqual(returned, new_blog)

    def test_blog_name_is_first_post_title(self):
        """Test case: blog name is first post title."""
        blog = Blog.objects.create()
        Post.objects.create(blog=blog, title='first post')
        Post.objects.create(blog=blog, title='second post')
        self.assertEqual(blog.name, 'first post')
