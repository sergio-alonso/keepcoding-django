"""Django blog app views."""

from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError

from blog.models import Blog, Post


def home_page(request):
    """Home page view."""
    return render(request, 'home.html')


def new_blog(request):
    """New blog page view."""
    blog = Blog.objects.create()
    post = Post(title=request.POST.get('post-title', ''), blog=blog)
    try:
        post.full_clean()
        post.save()
    except ValidationError:
        blog.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect('/blog/%d/' % (blog.id,))


def list_posts(request, blog_id):
    """List posts view."""
    blog = Blog.objects.get(id=blog_id)
    error = None

    if request.method == 'POST':
        try:
            post = Post(title=request.POST.get('post-title', ''), blog=blog)
            post.full_clean()
            post.save()
            return redirect('/blog/%d/' % (blog.id,))
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, 'list-posts.html', {'blog': blog, "error": error})
