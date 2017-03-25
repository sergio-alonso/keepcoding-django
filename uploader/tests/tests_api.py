import json
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import status

from uploader.models import Image


class ImageTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user.name@example.com', password='singlesecret')
        self.token = 'dXNlci5uYW1lQGV4YW1wbGUuY29tOnNpbmdsZXNlY3JldA=='

        self.anon_user = User.objects.create(email='no.name@example.com')
        self.anon_token = ''

    def tearDown(self):
        try:
            self.user.delete()

        except ObjectDoesNotExist:
            pass

        Image.objects.all().delete()

    def create_test_file(self, path):
        test_file = open(path, 'w')
        test_file.write('test_file\n')
        test_file.close()
        test_file = open(path, 'rb')
        return test_file

    def test_user_can_upload_a_file(self):
        url = '/api/v1/upload/'
        data = {'owner':self.user.email, 'file':self.create_test_file('/tmp/test_upload')}

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Basic ' + self.token)
        response = client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('id', response.data)
        self.assertEqual(response.data['owner'], self.user.email)

    def test_anonymous_user_can_not_upload(self):
        url = '/api/v1/upload/'
        data = {'owner':self.anon_user.email, 'file':self.create_test_file('/tmp/test_upload')}

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Basic ' + self.anon_token)
        response = client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(json.loads(response.content.decode('utf8')),
                         {"detail":"Invalid basic header. No credentials provided."})
