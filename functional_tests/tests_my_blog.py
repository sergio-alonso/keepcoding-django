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

    def test_logged_in_users_blog_are_saved_as_my_blogs(self):
        """Test case: logged in users blog are saved as my blog."""
        email = 'alice@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Alice is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
