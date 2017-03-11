"""Functional tests for authenticated users."""

import time

import django.test
import selenium.common.exceptions
import selenium.webdriver as webdriver
import selenium.webdriver.common.keys


class UserTest(django.test.LiveServerTestCase):
    """Authenticated User Tests."""

    MAXWAIT = 10

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
        inputbox.send_keys(selenium.webdriver.common.keys.Keys.ENTER)
        time.sleep(1)

        self.wait_for_row_in_list_table('My new blog post')

        # Then she sees that the site has generated a unique URL for her

        self.fail('Finish the test!')

    def test_multiple_users_can_start_blogs_at_different_urls(self):
        """Test case: multiple users can start blogs at different urls."""
        # Alice start a new blog
        self.browser.get(self.live_server_url + '/new-post')
        input = self.browser.find_element_by_class_name('post-title')
        input.send_keys('This is my first post')
        input.send_keys(webdriver.common.keys.Keys.ENTER)
        self.wait_for_row_in_list_table('This is my first post')

        # She notices that her blog has a unique URL
        alice_blog_url = self.browser.current_url
        self.assertRegex(alice_blog_url, '/blog/.+')

        # Now a new user, Bob, comes along to the site

        # We use a new browser session to make sure that no information
        # of Alice is coming through from cookies...

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Bob visits the new post page. There is no sign of Alice posts

        self.browser.get(self.live_server_url + '/new-post')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('This is my first post', body)

        # Bob starts new blog by entering a new post

        input = self.browser.find_element_by_class_name('post-title')
        input.send_keys('Lorem itsum')
        input.send_keys(webdriver.common.keys.Keys.ENTER)
        self.wait_for_row_in_list_table('Lorem itsum')

        # Bob gets its own unique URL

        bob_blog_url = self.browser.curses
        self.assertRegex(bob_blog_url, '/blog/.+')

        self.assertNotEqual(alice_blog_url, bob_blog_url)

        # Again, there is no trace of Alice posts

        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('This is my first post', body)
        self.assertIn('Lorem itsum', body)
