"""Django blog test forms."""
from django.test import TestCase
from blog.forms import PostForm, EMPTY_POST_TITLE_ERROR


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
