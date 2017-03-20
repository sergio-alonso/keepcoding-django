"""Functional tests for a blog."""

from django_seed import Seed
from django.contrib.auth import get_user_model
User = get_user_model()

from .functional_test import FunctionalTest
from blogs.models import Post

from selenium.webdriver.common.keys import Keys

ALICE_EMAIL = 'alice@example.com'
BOB_EMAIL = 'bob@example.com'


class BlogTest(FunctionalTest):
    """Test suite: blog test."""

    def test_display_a_list_of_last_posts(self):
        """Test case: display a list of last posts."""

        seeder = Seed.seeder()
        seeder.add_entity(User, 10)
        seeder.add_entity(Post, 20)
        seeder.execute()

        self.browser.get(self.live_server_url)

        self.wait_for(
            lambda: self.assertEqual(20, len(self.browser.find_elements_by_class_name('post-link')))
        )


    def test_display_a_list_of_existing_blogs(self):
        """Test case: display a list of existing blogs."""

        # Alice arrives to blog page
        self.browser.get(self.live_server_url + '/blogs/')

        # She can see a list of active blogs, none at this moment
        # and decide to create one for herself
        self.login(user_email=ALICE_EMAIL)
        self.wait_to_be_logged_in(email=ALICE_EMAIL)
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out(email=ALICE_EMAIL)

        self.restart_browser()

        # Bob arrives to blog page
        self.browser.get(self.live_server_url + '/blogs/')

        # He can see Alice's blog
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(ALICE_EMAIL)
        )

        # He decide to create one for himself
        self.login(user_email=BOB_EMAIL)
        self.wait_to_be_logged_in(email=BOB_EMAIL)
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out(email=BOB_EMAIL)

        # Now two blogs are listed
        self.browser.get(self.live_server_url + '/blogs/')
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(BOB_EMAIL)
        )
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(ALICE_EMAIL)
        )

        # Eight more people arrive and everyone creates a blog
        seeder = Seed.seeder()
        seeder.add_entity(User, 8)
        seeder.execute()

        self.browser.get(self.live_server_url + '/blogs/')
        self.wait_for(
            lambda: self.assertEqual(10, len(self.browser.find_elements_by_class_name('blog-link')))
        )

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

        # She is invited to enter a title, so she does.

        self.wait_for(
            lambda: self.browser.find_element_by_class_name('post-title')
        )
        self.browser.find_element_by_class_name('post-title').send_keys('My first post')
        self.browser.find_element_by_class_name('post-title').send_keys(Keys.ENTER)

        # Come back to her blog page after saving the post.

        self.wait_for(
            lambda: self.assertIn('/blogs/alice@example.com/', self.browser.current_url)
        )

        # Now she can see that her post is in there.

        self.wait_for(
            lambda: self.browser.find_element_by_link_text('My first post')
        )

        # WoW she can see it in detail.

        self.browser.find_element_by_link_text('My first post').click()
        self.wait_for(
            lambda: self.assertIn('/blogs/alice@example.com/21/', self.browser.current_url)
        )

        # She logs out. The "My blog" option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My blog'),
            []
        ))
