import json
from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.utils.timezone import now

from blogs.models import Post
from blogs.forms import EMPTY_POST_TITLE_ERROR, DUPLICATE_POST_TITLE_ERROR

class UserAPITest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create(email="admin@example.com", password='supersecret', is_admin=True)
        self.admin_header = {'HTTP_AUTHORIZATION': 'Basic {}'.format('YWRtaW5AZXhhbXBsZS5jb206c3VwZXJzZWNyZXQ=')}

        self.user = User.objects.create(email="user.name@example.com", password='singlesecret', is_admin=False)
        self.header = {'HTTP_AUTHORIZATION': 'Basic {}'.format('dXNlci5uYW1lQGV4YW1wbGUuY29tOnNpbmdsZXNlY3JldA==')}

        self.other_user = User.objects.create(email="bad.user@dummy.com", password='badsecret')
        self.other_header = {'HTTP_AUTHORIZATION': 'Basic {}'.format('YmFkLnVzZXJAZHVtbXkuY29tOmJhZHNlY3JldA==')}

        self.anon_header = {}


    def test_anonymous_user_can_create_an_account(self):
        response = self.client.post('/api/v1/user/', {'email':'dummy@example.com', 'password':'dummypass'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_avoid_duplicate_users_creation(self):
        response = self.client.post('/api/v1/user/', {'email':'dummy@example.com', 'password':'dummypass'})
        response = self.client.post('/api/v1/user/', {'email':'dummy@example.com', 'password':'dummypass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {"email": [
                "user with this email already exists."
            ]}
        )

    def test_a_user_can_only_list_itself(self):
        url = reverse('api:user-list')
        response = self.client.get(url, {}, **self.header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'email': 'user.name@example.com',
              'is_admin': False,
              'password': 'singlesecret',
              'posts': []}]
        )

    def test_admin_can_list_all_users(self):
        url = reverse('api:user-list')
        response = self.client.get(url, {}, **self.admin_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'email': 'admin@example.com',
              'is_admin': True,
              'password': 'supersecret',
              'posts': []},
             {'email': 'user.name@example.com',
              'is_admin': False,
              'password': 'singlesecret',
              'posts': []},
             {'email': 'bad.user@dummy.com',
              'is_admin': False,
              'password': 'badsecret',
              'posts': []}]
        )

    def test_anonymous_user_cannot_list_any_user(self):
        url = reverse('api:user-list')
        response = self.client.get(url, {}, **self.anon_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'detail': 'Authentication credentials were not provided.'}
        )

    def test_own_user_can_read_its_details(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.get(url, {}, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_read_all_users_details(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.get(url, {}, **self.admin_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_a_user_cannot_read_details_of_other_user(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.get(url, {}, **self.other_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_user_cannot_read_any_user_detail(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.get(url, {}, **self.anon_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_own_user_can_update_its_details(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.patch(url, data=urlencode({'is_admin':'True'}), content_type='application/x-www-form-urlencoded', **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_update_all_users_details(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.patch(url, data=urlencode({'is_admin':'True'}), content_type='application/x-www-form-urlencoded', **self.admin_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_a_user_cannot_update_details_of_other_user(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.patch(url, data=urlencode({'is_admin':'True'}), content_type='application/x-www-form-urlencoded', **self.other_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {"detail": "Not found."}
        )

    def test_anonymous_user_cannot_update_any_user_detail(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.patch(url, data=urlencode({'is_admin':'True'}), content_type='application/x-www-form-urlencoded', **self.anon_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {"detail": "Authentication credentials were not provided."}
        )


    def test_own_user_can_delete_itself(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.delete(url, **self.header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_user_can_delete_all_users(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.delete(url, **self.admin_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_a_user_cannot_delete_other_user(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.delete(url, **self.other_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {"detail": "Not found."}
        )

    def test_anonymous_user_cannot_delete_any_user(self):
        url = reverse('api:user-detail', args=[self.user.email])
        response = self.client.delete(url, **self.anon_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {"detail": "Authentication credentials were not provided."}
        )
