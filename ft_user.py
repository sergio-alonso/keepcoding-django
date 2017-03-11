"""Functional tests for authenticated users."""

import unittest

from selenium import webdriver


class UserTest(unittest.TestCase):
    """Authenticated User Tests."""

    def setUp(self):
        """Test case setUp."""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Test case tearDown."""
        self.browser.quit()

    def test_can_create_a_new_post(self):
        """Test Case: create a new post."""
        # Alice wants to create a new post.
        self.browser.get('http://localhost:8000/new-post')

        # She notices the page title and header mention resource lists
        self.assertIn('Nueva entrada en el blog', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Nueva entrada en el blog', header_text)

        # She is invited to enter a post title straight away

        # She types "My new blog post" into a text box

        # When she hits enter, the page updates, and now the page lists
        # "My new blog posts" as a post in a blog list

        # Then she sees that the site has generated a unique URL for her

        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
