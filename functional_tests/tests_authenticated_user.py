"""Functional tests for authenticated users."""

import time

import django.test.LiveServerTestCase as LiveServerTestCase
import selenium.webdriver as webdriver
import selenium.webdriver.common.keys.Keys as Keys


class UserTest(LiveServerTestCase):
    """Authenticated User Tests."""

    def setUp(self):
        """Test case setUp."""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Test case tearDown."""
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """Check if a text exists as table row."""
        table = self.browser.find_element_by_class_name('post-list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row_text for row in rows])

    def test_can_create_a_new_post(self):
        """Test Case: create a new post."""
        # Alice wants to create a new post.
        self.browser.get(self.live_server_url + '/new-post')

        # She notices the page title and header mention resource lists
        self.assertIn('Nueva entrada en el blog', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Nueva entrada en el blog', header_text)

        # She is invited to enter a post title straight away
        inputbox = self.browser.find_element_by_class_name('post-title')

        # She types "My new blog post" into a text box
        inputbox.send_keys('My new blog post')

        # When she hits enter, the page updates, and now the page lists
        # "My new blog posts" as a post in a blog list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('My new blog post')

        # Then she sees that the site has generated a unique URL for her

        self.fail('Finish the test!')
