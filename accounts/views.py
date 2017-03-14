"""Django accounts views."""
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from accounts.models import Token


def send_login_email(request):
    """Send login email."""
    email = request.POST.get('email', '')
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
                reverse('login') + '?token=' + str(token.uid)
    )
    send_mail(
        'Your login link for KeepCoding Django',
        'Use this link to log in:\n\n%s' % url,
        'noreply@example.com',
        [email],
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    """Login."""
    uid = request.GET.get('token')
    user = auth.authenticate(uid=uid)
    if user:
        auth.login(request, user)
    return redirect('/')
