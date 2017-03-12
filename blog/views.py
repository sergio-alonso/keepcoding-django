"""Django blog app views."""

from django.shortcuts import redirect, render

from blog.models import Blog, Post


def home_page(request):
    """Home page view."""
    return render(request, 'home.html')


def new_post_page(request):
    """New post page view."""
    if request.method == 'POST':
        blog = Blog.objects.create()
        Post.objects.create(title=request.POST.get('post-title', ''), blog=blog)
        return redirect('/blog/%d/' % (blog.id,))

    return render(request, 'new-post.html')


def list_posts(request, blog_id):
    """List posts view."""
    blog = Blog.objects.get(id=blog_id)
    posts = Post.objects.filter(blog=blog)
    return render(request, 'list-posts.html', {'posts': posts})


def new_blog(request):
    """New blog."""
    blog = Blog.objects.create()
    Post.objects.create(title=request.POST.get('post-title', ''), blog=blog)
    return redirect('/blogs/%d/' % (blog.id,))
