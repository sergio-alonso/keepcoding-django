"""Django blog app views."""

from blog.models import Blog, Post
from django.shortcuts import redirect, render


def home_page(request):
    """Home page view."""
    return render(request, 'home.html')


def new_post_page(request):
    """New post page view."""
    if request.method == 'POST':
        blog = Blog.objects.create()
        Post.objects.create(title=request.POST.get('post-title', ''), blog=blog)
        return redirect('/blog/the-only-blog-in-the-world/')

    return render(request, 'new-post.html')


def list_posts(request):
    """List posts view."""
    posts = Post.objects.all()
    return render(request, 'list-posts.html', {'posts': posts})


def new_blog(request):
    """New blog."""
    blog = Blog.objects.create()
    Post.objects.create(title=request.POST.get('post-title', ''), blog=blog)
    return redirect('/blogs/the-only-blog-in-the-world/')
