"""Blog views."""

from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
User = get_user_model()

from blogs.forms import PostForm, NewPostForm
from blogs.models import Post

def home(request):
    """Home view."""
    return render(request, 'home.html')


def blog(request, user_email):
    """Blog view."""
    owner = User.objects.get(email=user_email)
    return render(request, 'blog.html', {'owner': owner})

def post_create(request):
    """Post create view."""
    return render(request, 'post_create.html', {'form': PostForm()})


def post_save(request):
    """Post save view."""
    form = NewPostForm(data=request.POST)
    if form.is_valid():
        post = form.save(owner=request.user)
        return redirect('blog', user_email=request.user.email)
    return render(request, 'post_create.html', {'form': NewPostForm()})


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class BlogsListView(ListView):
    model = User
    template_name = 'blogs_list.html'
