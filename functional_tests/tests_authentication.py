"""Functional tests for authentication."""

from .functional_test import FunctionalTest

ALICE_EMAIL = 'alice@example.com'
BOB_EMAIL = 'bob@example.com'


class AuthenticationTest(FunctionalTest):
    """Test suite: authentication."""

    def test_can_get_email_link_to_log_in(self):
        """Test case: can get email link to log in."""
        #
        # Alice goes to the awesome KeepCoding Django new site.
        # She goes to check out its homepage.

        self.browser.get(self.live_server_url)

        # She notices a "Log in" section in the navigation bar for the first time.
        # It's telling her to enter her email address, so she does.

        self.login(user_email=ALICE_EMAIL)

        # She is logged in!

        self.wait_to_be_logged_in(email=ALICE_EMAIL)

        # She notices that her blog has a unique URL

        alice_blog_url = self.browser.current_url
        self.assertRegex(alice_blog_url, '/blogs/.+')

        # The url include her email.

        self.assertIn(ALICE_EMAIL, alice_blog_url)

        # Now she logs out.

        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out!

        self.wait_to_be_logged_out(email=ALICE_EMAIL)

        #
        # Now a new user, Bob, comes along to the site

        # We use a new browser session to make sure that no information
        # of Alice is coming through from cookies...

        self.restart_browser()

        # Bob visits the new post page.

        self.browser.get(self.live_server_url)

        # Bob gets its own unique URL

        self.login(user_email=BOB_EMAIL)
        bob_blog_url = self.browser.current_url
        self.assertRegex(bob_blog_url, '/blogs/.+')

        # The url include his email.

        self.assertIn(BOB_EMAIL, bob_blog_url)

        # That is different from Alice's url

        self.assertNotEqual(alice_blog_url, bob_blog_url)

        # And, satisfied, he logs out.
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out(email=BOB_EMAIL)
