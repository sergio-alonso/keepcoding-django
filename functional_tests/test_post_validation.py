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
        self.get_post_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the
        # list page
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # She starts typing some text for the new item and the error disappears
        self.get_post_input_box().send_keys('First post')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # And she can submit it successfully
        self.get_post_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_post_table('First post')

        # Perversely, she now decides to submit a second blank blog post
        self.get_post_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        self.wait_for_row_in_post_table('First post')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # And she can correct it by filling some text in
        self.get_post_input_box().send_keys('Second post')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_post_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_post_table('First post')
        self.wait_for_row_in_post_table('Second post')
