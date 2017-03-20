"""Functional tests commons."""

import time
import re

import selenium.common.exceptions
import selenium.webdriver as webdriver

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.core import mail

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from django.conf import settings

User = get_user_model()

MAX_WAIT = 10

def wait(fn):
    """Wait."""
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """Functional Tests."""

    @classmethod
    def setUp(self):
        """Test case setUp."""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Test case tearDown."""
        self.browser.quit()

    def restart_browser(self):
        """Restart browser."""
        self.browser.quit()
        self.browser = webdriver.Firefox()

    @wait
    def wait_for(self, fn):
        """Wait for."""
        return fn()

    @wait
    def wait_to_be_logged_in(self, email):
        """Wait to be logged in."""
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        """Wait to be logged out."""
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def login(self, user_email):
        """Login."""

        # Enter the email address.

        self.browser.find_element_by_name('email').send_keys(user_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling that an email has been sent.

        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Checks the email client to find a message.

        email = mail.outbox[-1]
        self.assertIn(user_email, email.to)
        self.assertEqual(email.subject, "Your login link for KeepCoding Django")

        # It has an url link in it.

        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail('Could not find url in email body:\n%s' % email.body)
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Clicks it.

        self.browser.get(url)

    def create_pre_authenticated_session(self, email):
        """Create pre authenticated session."""
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # to set a cookie we need to first visit the domain.
        # 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))


    # @wait
    # def wait_for_row_in_post_table(self, row_text):
    #     """Check if a text exists as table row."""
    #     table = self.browser.find_element_by_class_name('post-list')
    #     rows = table.find_elements_by_tag_name('tr')
    #     self.assertIn(row_text, [row.text for row in rows])

    # def get_post_input_box(self):
    #     """Get post title."""
    #     return self.browser.find_element_by_id('id_title')

    # def add_blog_post(self, post_title):
    #     """Add blog post."""
    #     self.get_post_input_box().send_keys(post_title)
    #     self.get_post_input_box().send_keys(Keys.ENTER)
    #     self.wait_for_row_in_post_table(
    #         '{}'.format(post_title)
    #     )
