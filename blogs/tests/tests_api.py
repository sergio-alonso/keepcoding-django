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

class BlogAPITest(TestCase):

    def setUp(self):
        User.objects.create(email="user.name.0@example.com")
        User.objects.create(email="user.name.1@example.com")
        User.objects.create(email="user.name.2@example.com")
        User.objects.create(email="user.name.3@example.com")
        User.objects.create(email="user.name.4@example.com")


    def test_blog_list(self):
        url = reverse('api:blogs-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'posts_count': 0, 'blog': '/api/v1/blogs/user.name.0@example.com/'},
             {'posts_count': 0, 'blog': '/api/v1/blogs/user.name.1@example.com/'},
             {'posts_count': 0, 'blog': '/api/v1/blogs/user.name.2@example.com/'},
             {'posts_count': 0, 'blog': '/api/v1/blogs/user.name.3@example.com/'},
             {'posts_count': 0, 'blog': '/api/v1/blogs/user.name.4@example.com/'}]
        )


    def test_blog_search_by_username(self):
        url = reverse('api:blogs-list')
        response = self.client.get(url, {'search':'name.2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'posts_count': 0, 'blog': '/api/v1/blogs/user.name.2@example.com/'}]
        )


class PostAPITest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create(email="admin@example.com", password='supersecret', is_admin=True)
        self.admin_header = {'HTTP_AUTHORIZATION': 'Basic {}'.format('YWRtaW5AZXhhbXBsZS5jb206c3VwZXJzZWNyZXQ=')}

        self.user = User.objects.create(email="user.name@example.com", password='singlesecret', is_admin=False)
        self.user_header = {'HTTP_AUTHORIZATION': 'Basic {}'.format('dXNlci5uYW1lQGV4YW1wbGUuY29tOnNpbmdsZXNlY3JldA==')}

        post1 = Post.objects.create(title='Post 5', summary='Post A', owner=self.user, published_date='2017-01-01T00:00:00.000000Z')
        Post.objects.create(title='Post 4', summary='Post B', owner=self.user)
        Post.objects.create(title='Post 3', summary='Post C', owner=self.user, published_date='2017-01-02T00:00:00.000000Z')
        Post.objects.create(title='Post 2', summary='Post D', owner=self.user)
        Post.objects.create(title='Post 1', summary='Post E', owner=self.user, published_date='2017-01-03T00:00:00.000000Z')

        post1.category.add("category-1")

        self.other_user = User.objects.create(email="bad.user@dummy.com", password='badsecret')
        self.other_header = {'HTTP_AUTHORIZATION': 'Basic {}'.format('YmFkLnVzZXJAZHVtbXkuY29tOmJhZHNlY3JldA==')}

        self.anon_header = {}

    def test_anonymous_user_can_only_read_published_posts(self):
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.get(url, **self.anon_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_other_user_can_only_read_published_posts(self):
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.get(url, **self.other_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_owner_can_read_all_posts(self):
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.get(url, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_owner_can_search_by_title(self):
        url = reverse('api:post-list', args=[self.user.email])
        data = {'search':'2'}
        response = self.client.get(url, data, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'}]
        )

    def test_owner_can_search_by_summary(self):
        url = reverse('api:post-list', args=[self.user.email])
        data = {'search':'B'}
        response = self.client.get(url, data, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'}]
        )

    def test_user_can_search_by_category(self):
        url = reverse('api:post-list', args=[self.user.email])
        data = {'category':'category-1'}
        response = self.client.get(url, data, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_owner_post_are_sorted_by_inverse_published_date(self):
        # First published is last displayed
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.get(url, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_owner_can_sort_all_post_by_title(self):
        url = reverse('api:post-list', args=[self.user.email])
        data = {'ordering':'title'}
        response = self.client.get(url, data, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_owner_can_sort_all_post_by_published_date(self):
        url = reverse('api:post-list', args=[self.user.email])
        data = {'ordering':'published_date'}
        response = self.client.get(url, data, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'}]
        )

    def test_user_can_create_a_new_post(self):
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.post(url, data=urlencode({'title':'new post'}), content_type='application/x-www-form-urlencoded', **self.user_header)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            json.loads(response.content.decode('utf8'))['title'], 'new post'
        )

        # TODO: mock now
        #
        # verify that user posts has been created
        # url = reverse('api:post-list', args=[self.user.email])
        # response = self.client.get(url, **self.user_header)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertRegex(
        #     json.loads(response.content.decode('utf8')),
        #     [{'category': [], 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
        #      {'category': [], 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
        #      {'category': [], 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
        #      {'category': [], 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'},
        #      {'category': ['category-1'], 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'},
        #      {'category': [], 'imagen': '', 'published_date': '(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z', 'summary': '', 'title': 'new post'}]
        # )

    def test_other_user_can_not_create_a_new_post_in_others_blog(self):
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.post(url, data=urlencode({'title':'new post'}), content_type='application/x-www-form-urlencoded', **self.other_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'detail': 'You do not have permission to perform this action.'}
        )

        # verify that user posts has not been created
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.get(url, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_anonymous_user_can_not_create_a_new_post(self):
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.post(url, data=urlencode({'title':'new post'}), content_type='application/x-www-form-urlencoded', **self.anon_header)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'detail': 'Authentication credentials were not provided.'}
        )

        # verify that user posts has not been created
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.get(url, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_user_can_read_all_its_own_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 2])
        response = self.client.get(url, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'}
        )

    def test_admin_can_read_any_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 2])
        response = self.client.get(url, **self.admin_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'}
        )

    def test_other_user_can_read_any_published_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 1])
        response = self.client.get(url, **self.other_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}
        )

    def test_other_user_can_not_read_others_private_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 2])
        response = self.client.get(url, **self.other_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {"detail": "Not found."}
        )

    def test_anonymous_can_read_published_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 1])
        response = self.client.get(url, **self.anon_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}
        )

    def test_anonymous_can_not_read_private_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 2])
        response = self.client.get(url, **self.anon_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {"detail": "Not found."}
        )

    def test_user_can_update_its_own_post_details(self):
        url = reverse('api:post-detail', args=[self.user.email, 2])
        response = self.client.patch(url, data=urlencode({'summary':'something'}), content_type='application/x-www-form-urlencoded', **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'something', 'title': 'Post 4'}
        )

    def test_admin_can_update_any_post_details(self):
        url = reverse('api:post-detail', args=[self.user.email, 2])
        response = self.client.patch(url, data=urlencode({'summary':'another thing'}), content_type='application/x-www-form-urlencoded', **self.admin_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'another thing', 'title': 'Post 4'}
        )

    def test_other_user_can_not_update_any_other_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 1])
        response = self.client.patch(url, data=urlencode({'summary':'another thing'}), content_type='application/x-www-form-urlencoded', **self.other_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'detail': 'You do not have permission to perform this action.'}
        )

    def test_anonymous_can_not_update_any_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 1])
        response = self.client.patch(url, data=urlencode({'summary':'another thing'}), content_type='application/x-www-form-urlencoded', **self.anon_header)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'detail': 'Authentication credentials were not provided.'}
        )

    def test_user_can_delete_its_own_posts(self):
        url = reverse('api:post-detail', args=[self.user.email, 2])
        response = self.client.delete(url, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # verify that user posts has been removed
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.get(url, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_admin_can_delete_any_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 2])
        response = self.client.delete(url, **self.admin_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # verify that user posts has been removed
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.get(url, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_other_user_can_not_delete_any_others_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 1])
        response = self.client.delete(url, **self.other_header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'detail': 'You do not have permission to perform this action.'}
        )

        # verify that user has all posts
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.get(url, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )

    def test_anonymous_can_not_delete_any_post(self):
        url = reverse('api:post-detail', args=[self.user.email, 1])
        response = self.client.delete(url, **self.anon_header)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'detail': 'Authentication credentials were not provided.'}
        )

        # verify that user has all posts
        url = reverse('api:post-list', args=[self.user.email])
        response = self.client.get(url, **self.user_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [{'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-03T00:00:00Z', 'summary': 'Post E', 'title': 'Post 1'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post D', 'title': 'Post 2'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-02T00:00:00Z', 'summary': 'Post C', 'title': 'Post 3'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': None, 'summary': 'Post B', 'title': 'Post 4'},
             {'author': 'user.name@example.com', 'imagen': '', 'published_date': '2017-01-01T00:00:00Z', 'summary': 'Post A', 'title': 'Post 5'}]
        )
