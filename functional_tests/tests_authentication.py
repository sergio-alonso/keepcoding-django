"""Functional tests for authentication."""
import re

from django.core import mail
from selenium.webdriver.common.keys import Keys


from .functional_test import FunctionalTest

class AuthenticationTest(FunctionalTest):
    """Test suite: authentication."""

    def test_can_get_email_link_to_log_in(self):
        """Test case: can get email link to log in."""
        # Alice goes to the awesome KeepCoding Django new site
        # and notices a "Log in" section in the navigation bar for the first time.
        # It's telling her to enter her email address, so dhe does.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her that an email has been sent.
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her email and finds a message.
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has an url link in it.
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail('Could not find url in email body:\n%s' % email.body)
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it.
        self.browser.get(url)

        # She is logged in!
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # Now she logs out.
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out!
        self.wait_to_be_logged_out(email=TEST_EMAIL)
