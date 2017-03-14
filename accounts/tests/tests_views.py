"""Django accounts view tests."""
from django.test import TestCase
from unittest.mock import patch, call
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    """Test suite: send login email view."""

    def test_redirects_to_home_page(self):
        """Test case: redirects to home page."""
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'user.name@example.com'
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        """Test cas: sends mail to address from post."""
        self.client.post('/accounts/send_login_email', data={
            'email': 'user.name@example.com'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for KeepCoding Django')
        self.assertEqual(from_email, 'noreply@example.com')
        self.assertEqual(to_list, ['user.name@example.com'])

    def test_adds_success_message(self):
        """Test case: adds success message."""
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'user.name@example.com'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_with_email(self):
        """Test case: creates token associated with email."""
        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        """Test cas: sends link to login using tocken uid."""
        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        token = Token.objects.first()
        expected_url = 'http://testserver/accounts/login?token=%s' % token.uid
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    """Test suite: login view."""

    def test_redirects_to_home_page(self, mock_auth):
        """Test case: redirects to home page."""
        response = self.client.get('/accounts/login?token=abc123')
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        """Test case: calls authenticate with uid from get request."""
        self.client.get('/accounts/login?token=abc123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abc123')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        """Test case: calls auth login with user if there is one."""
        response = self.client.get('/accounts/login?token=abc123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        """Test case: does not login if user is not authenticated."""
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abc123')
        self.assertEqual(mock_auth.login.called, False)
