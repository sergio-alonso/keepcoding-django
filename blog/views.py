"""Django blog views."""
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from blog.forms import PostForm, NewBlogForm
from blog.models import Blog

User = get_user_model()


def home_page(request):
    """Home view."""
    return render(request, 'home.html', {'form': PostForm()})


def new_blog(request):
    """New blog."""
    form = NewBlogForm(data=request.POST)
    if form.is_valid():
        blog = form.save(owner=request.user)
        return redirect(blog)
    return render(request, 'home.html', {'form': form})


def list_posts(request, blog_id):
    """List posts view."""
    blog = Blog.objects.get(id=blog_id)
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            form.save(for_blog=blog)
            return redirect(blog)
    return render(request, 'list-posts.html', {'blog': blog, "form": form})


def my_blog(request, email):
    """My blog."""
    owner = User.objects.get(email=email)
    return render(request, 'my_blog.html', {'owner': owner})
