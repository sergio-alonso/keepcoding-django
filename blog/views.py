"""Django blog app views."""

from django.shortcuts import redirect, render

from blog.models import Blog, Post


def home_page(request):
    """Home page view."""
    return render(request, 'home.html')


def new_blog(request):
    """New blog page view."""
    blog = Blog.objects.create()
    Post.objects.create(title=request.POST.get('post-title', ''), blog=blog)
    return redirect('/blog/%d/' % (blog.id,))


def add_post(request, blog_id):
    """Add post."""
    blog = Blog.objects.get(id=blog_id)
    Post.objects.create(title=request.POST.get('post-title', ''), blog=blog)
    return redirect('/blog/%d/' % (blog.id,))


def list_posts(request, blog_id):
    """List posts view."""
    blog = Blog.objects.get(id=blog_id)
    return render(request, 'list-posts.html', {'blog': blog})
