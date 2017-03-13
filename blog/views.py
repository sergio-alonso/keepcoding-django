"""Django blog views."""
from django.shortcuts import redirect, render

from blog.forms import PostForm
from blog.models import Blog


def home_page(request):
    """Home view."""
    return render(request, 'home.html', {'form': PostForm()})


def new_blog(request):
    """New blog view."""
    form = PostForm(data=request.POST)
    if form.is_valid():
        blog = Blog.objects.create()
        form.save(for_blog=blog)
        return redirect(blog)
    else:
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
