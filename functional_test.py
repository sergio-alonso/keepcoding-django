"""Check that we have Django installed."""


import unittest

from selenium import webdriver


class AnonymousUserTest(unittest.TestCase):
    """Anonymous User Test."""

    def setUp(self):
        """Test case setUp."""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Test case tearDown."""
        self.browser.quit()

    def test_can_browse_last_created_posts(self):
        """Test Case: list last post on home page."""
        # Alice has heard about a cool new online app.
        # She goes to check out its homepage.
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention resource lists
        self.assertIn('Recursos', self.browser.title)

        # And the page lists last post published by another users
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
