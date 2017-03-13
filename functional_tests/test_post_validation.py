"""Functional tests for authenticated users."""
from .functional_test import FunctionalTest


class PostValidationTest(FunctionalTest):
    """Post Validation Test."""

    def test_cannot_add_empty_blog_posts(self):
        """Test case: cannot add empty blog posts."""
        # Alice goes to the home page and accidentally tries to submit
        # an empty blog post. She hits Enter on the empty input box

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank

        # She tries again with some text for the item, which now works

        # Perversely, she now decides to submit a second blank blog post

        # She receives a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail('write me!')
