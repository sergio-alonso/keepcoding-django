"""Functional tests for authenticated users."""
from .functional_test import FunctionalTest

import selenium.webdriver as webdriver
import selenium.webdriver.common.keys


class NewVisitorTest(FunctionalTest):
    """New Visitor Test."""

    def test_can_start_a_blog_for_one_user(self):
        """Test Case: list last post on home page."""
#        # Alice has heard about a cool new online app.
#        # She goes to check out its homepage.
#        self.browser.get(self.live_server_url)

#        # She notices the page title and header mention resource lists
#        self.assertIn('KeepCoding - Django', self.browser.title)
#        header_text = self.browser.find_element_by_tag_name('h1').text
#        self.assertIn('Start a new blog', header_text)

#        # She is invited to enter a post title straight away
#        inputbox = self.get_post_input_box()
#        self.assertEqual(
#            inputbox.get_attribute('placeholder'),
#            'Enter a post title'
#        )

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys('My first post')
        inputbox.send_keys(selenium.webdriver.common.keys.Keys.ENTER)
        self.wait_for_row_in_post_table('My first post')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.get_post_input_box()
        inputbox.send_keys('My second post')
        inputbox.send_keys(selenium.webdriver.common.keys.Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_post_table('My second post')
        self.wait_for_row_in_post_table('My first post')

    def test_multiple_users_can_start_blogs_at_different_urls(self):
        """Test case: multiple users can start blogs at different urls."""
        # Alice start a new blog
        self.browser.get(self.live_server_url)
        input = self.get_post_input_box()
        input.send_keys('This is my first post')
        input.send_keys(webdriver.common.keys.Keys.ENTER)
        self.wait_for_row_in_post_table('This is my first post')

        # She notices that her blog has a unique URL
        alice_blog_url = self.browser.current_url
        self.assertRegex(alice_blog_url, '/blog/.+')

        # Now a new user, Bob, comes along to the site

        # We use a new browser session to make sure that no information
        # of Alice is coming through from cookies...

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Bob visits the new post page. There is no sign of Alice posts

        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('This is my first post', body)

        # Bob starts new blog by entering a new post

        input = self.get_post_input_box()
        input.send_keys('Lorem itsum')
        input.send_keys(webdriver.common.keys.Keys.ENTER)
        self.wait_for_row_in_post_table('Lorem itsum')

        # Bob gets its own unique URL

        bob_blog_url = self.browser.current_url
        self.assertRegex(bob_blog_url, '/blog/.+')

        self.assertNotEqual(alice_blog_url, bob_blog_url)

        # Again, there is no trace of Alice posts

        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('This is my first post', body)
        self.assertIn('Lorem itsum', body)
