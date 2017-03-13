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

    def wait_for_row_in_list_table(self, row_text):
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
