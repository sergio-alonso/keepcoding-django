"""Django blog app views."""
from django.shortcuts import render


def home_page(request):
    """Home page view."""
    return render(request, 'home.html')


def new_post_page(request):
    """New post page view."""
    return render(request, 'new-post.html', {
        'new_post_title': request.POST.get('post-title'),
    })
