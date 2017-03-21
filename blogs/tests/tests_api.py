import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
User = get_user_model()

from blogs.models import Post
from blogs.forms import EMPTY_POST_TITLE_ERROR, DUPLICATE_POST_TITLE_ERROR

class UserAPITest(TestCase):

    def test_get_returns_json_200(self):
        user = User.objects.create(email='user.name@example.com')
        post = Post.objects.create(title='New post', owner=user)
        url = reverse('api:post-detail', args=[post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_posts_for_correct_user(self):
        other_user = User.objects.create(email='other.user@example.com')
        Post.objects.create(owner=other_user, title='post 0')
        our_user = User.objects.create(email='our.user@example.com')
        post1 = Post.objects.create(owner=our_user, title='post 1')
        post2 = Post.objects.create(owner=our_user, title='post 2')

        url = reverse('api:user-detail', args=[our_user.email])
        response = self.client.get(url)

        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'email': our_user.email, 'posts': [
                {'id': post1.id, 'title': post1.title, 'owner': our_user.email},
                {'id': post2.id, 'title': post2.title, 'owner': our_user.email},
            ]}
        )


class PostAPITest(TestCase):
    base_url = reverse('api:post-list')

    def setUp(self):
        self.user = User.objects.create(email="user.name@example.com")

    def test_POSTing_a_new_post(self):
        response = self.client.post(
            self.base_url,
            {'owner': self.user.email, 'title': 'new post'},
        )
        self.assertEqual(response.status_code, 201)
        new_post = self.user.post_set.get()
        self.assertEqual(new_post.title, 'new post')

    def post_empty_input(self):
        return self.client.post(
            self.base_url,
            data={'owner': self.user.email, 'title': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_empty_input()
        self.assertEqual(Post.objects.count(), 0)

    def test_for_invalid_input_returns_error_code(self):
        response = self.post_empty_input()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'title': [EMPTY_POST_TITLE_ERROR]}
        )

    def test_duplicate_posts_error(self):
        self.client.post(self.base_url, data={'owner': self.user.email, 'title': 'duplicate!'})
        response = self.client.post(self.base_url, data={'owner': self.user.email, 'title': 'duplicate!'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'non_field_errors': [DUPLICATE_POST_TITLE_ERROR]}
        )
