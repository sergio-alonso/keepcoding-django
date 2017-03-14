"""Functional tests for authenticated users."""
import time

import selenium.common.exceptions
import selenium.webdriver as webdriver
import selenium.webdriver.common.keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class FunctionalTest(StaticLiveServerTestCase):
    """Functional Tests."""

    MAXWAIT = 10

    @classmethod
    def setUp(self):
        """Test case setUp."""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Test case tearDown."""
        self.browser.quit()

    def wait_for_row_in_post_table(self, row_text):
        """Check if a text exists as table row."""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_class_name('post-list')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, selenium.common.exceptions.WebDriverException) as e:
                if time.time() - start_time > self.MAXWAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        """Check if a text exists as table row."""
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, selenium.common.exceptions.WebDriverException) as e:
                if time.time() - start_time > self.MAXWAIT:
                    raise e
                time.sleep(0.5)

    def get_post_input_box(self):
        """Get post title."""
        return self.browser.find_element_by_id('id_title')

    def wait_to_be_logged_in(self, email):
        """Wait to be logged in."""
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Log out')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        """Wait to be logged out."""
        self.wait_for(
            lambda: self.browser.find_element_by_name('email')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
