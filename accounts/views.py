"""Django accounts views."""
import sys
import uuid

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from accounts.models import Token


def send_login_email(request):
    """Send login email."""
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri('/accounts/login?uid=%s' % uid)
    send_mail(
        'Your login link for KeepCoding Django',
        'Use this link to log in:\n\n%s' % url,
        'noreply@example.com',
        [email],
    )
    return render(request, 'login_email_sent.html')


def login(request):
    """Login."""
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
        return redirect('/')


def logout(request):
    """Logout."""
    auth_logout(request)
    return redirect('/')
