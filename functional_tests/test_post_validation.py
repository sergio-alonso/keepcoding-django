"""Functional tests for authenticated users."""
from selenium.webdriver.common.keys import Keys

from .functional_test import FunctionalTest


class PostValidationTest(FunctionalTest):
    """Post Validation Test."""

    def test_cannot_add_empty_blog_posts(self):
        """Test case: cannot add empty blog posts."""
        # Alice goes to the home page and accidentally tries to submit
        # an empty blog post. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('post-title').send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # She tries again with some text for the item, which now works
        self.browser.find_element_by_class_name('post-title').send_keys('First post')
        self.browser.find_element_by_class_name('post-title').send_keys(Keys.ENTER)
        self.wait_for_row_in_post_table('First post')

        # Perversely, she now decides to submit a second blank blog post
        self.browser.find_element_by_class_name('post-title').send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # And she can correct it by filling some text in
        self.browser.find_element_by_css_selector('post-title').send_keys('Second post')
        self.browser.find_element_by_css_selector('post-title').send_keys(Keys.ENTER)
        self.wait_for_row_in_post_table('First post')
        self.wait_for_row_in_post_table('Second post')
