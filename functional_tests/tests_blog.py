"""Functional tests for a blog."""

from .functional_test import FunctionalTest


class BlogTest(FunctionalTest):
    """Test suite: blog test."""

    def test_logged_in_users_blog_are_saved_as_my_blog(self):
        """Test case: logged in users blog are saved as my blog."""
        # Alice is a logged-in user

        self.create_pre_authenticated_session('alice@example.com')

        # She goes to her blog page

        self.browser.get(self.live_server_url + '/blogs/alice@example.com/')

        # She notices a "My blog" link, that takes her to the same page! :)

        self.browser.find_element_by_link_text('My blog').click()
        self.wait_for(
            lambda: self.assertIn('/blogs/alice@example.com/', self.browser.current_url)
        )

        # And a message of no post at the bottom.

        self.wait_for(
            lambda: self.browser.find_element_by_class_name('posts-count')
        )
        posts_count = self.browser.find_element_by_class_name('posts-count').text
        self.assertEqual('No posts', posts_count)

        # She decides to start a post, just to see.
        self.browser.find_element_by_link_text('Create a new post').click()

        # A new page appears, with a form to create a post
        self.wait_for(
            lambda: self.assertIn('/new-post', self.browser.current_url)
        )

        # She sees that her blog is in there, named according to its
        # first blog post
        #self.wait_for(
        #    lambda: self.browser.find_element_by_link_text('First post')
        #)
        #self.browser.find_element_by_link_text('First post').click()
        #self.wait_for(
        #    lambda: self.assertEqual(self.browser.current_url, first_post_url)
        #)

        # She logs out. The "My blog" option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My blog'),
            []
        ))
