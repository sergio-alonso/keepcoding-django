"""Blog views."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
User = get_user_model()

from blogs.forms import PostForm, NewPostForm
from blogs.models import Post

class Home(ListView):
    """Home view."""
    queryset = Post.objects.order_by('-published_date')
    template_name = "home.html"


def blog(request, user_email):
    """Blog view."""
    owner = User.objects.get(email=user_email)
    posts = Post.objects.filter(owner=owner).select_related().order_by('-published_date')

    return render(request, 'blog.html', {'owner': owner, 'posts':posts})

@login_required
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
