"""Django my blog tests."""
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .functional_test import FunctionalTest
User = get_user_model()


class MyBlogTest(FunctionalTest):
    """Test suite: my blog test."""

    def create_pre_authenticated_session(self, email):
        """Test case: create pre authenticated session."""
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

    def test_logged_in_users_blog_are_saved_as_my_blog(self):
        """Test case: logged in users blog are saved as my blog."""
        # Alice is a logged-in user
        self.create_pre_authenticated_session('alice@example.com')

        # She goes to the home page and starts a blog post
        self.browser.get(self.live_server_url)
        self.add_blog_post('First post')
        self.add_blog_post('Second post')
        first_post_url = self.browser.current_url

        # She notices a "My blog" link, for the first time.
        self.browser.find_element_by_link_text('My blog').click()

        # She sees that her blog is in there, named according to its
        # first blog post
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('First post')
        )
        self.browser.find_element_by_link_text('First post').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_post_url)
        )
        # She decides to start another post, just to see
        self.browser.get(self.live_server_url)
        self.add_blog_post('Third post')
        second_post_url = self.browser.current_url

        # Under "My blog", her new post appears
        self.browser.find_element_by_link_text('My blog').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Third post')
        )
        self.browser.find_element_by_link_text('third post').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_post_url)
        )
        # She logs out.  The "My blog" option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My blog'),
            []
        ))
