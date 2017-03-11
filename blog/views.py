"""Django blog app views."""

from django.shortcuts import redirect, render

from blog.models import Post


def home_page(request):
    """Home page view."""
    return render(request, 'home.html')


def new_post_page(request):
    """New post page view."""
    if request.method == 'POST':
        Post.objects.create(title=request.POST.get('post-title', ''))
        return redirect('/new-post/')

    posts = Post.objects.all()
    return render(request, 'new-post.html', {'posts': posts})
