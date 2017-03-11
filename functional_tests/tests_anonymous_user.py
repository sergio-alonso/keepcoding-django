"""Check that we have Django installed."""

from django.test import LiveServerTestCase
from selenium import webdriver


class AnonymousUserTest(LiveServerTestCase):
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
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention resource lists
        self.assertIn('Recursos', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Recursos', header_text)

        # And the page lists last post published by another users
        table = self.browser.find_element_by_id('main')
        rows = table.find_elements_by_tag_name('article')
        self.assertTrue(
            any(row.text == 'Articulo 1' for row in rows)
        )

        self.fail('Finish the test!')
