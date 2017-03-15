"""Functional tests for authenticated users."""
import time

import selenium.common.exceptions
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

MAX_WAIT = 10


def wait(fn):
    """Wait."""
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, selenium.common.exceptions.WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """Functional Tests."""

    @classmethod
    def setUp(self):
        """Test case setUp."""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Test case tearDown."""
        self.browser.quit()

    @wait
    def wait_for(self, fn):
        """Wait for."""
        return fn()

    @wait
    def wait_for_row_in_post_table(self, row_text):
        """Check if a text exists as table row."""
        table = self.browser.find_element_by_class_name('post-list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_post_input_box(self):
        """Get post title."""
        return self.browser.find_element_by_id('id_title')

    @wait
    def wait_to_be_logged_in(self, email):
        """Wait to be logged in."""
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        """Wait to be logged out."""
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def add_blog_post(self, post_title):
        """Add blog post."""
        self.get_post_input_box().send_keys(post_title)
        self.get_post_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_post_table(
            '{}'.format(post_title)
        )
