"""Blog views."""

from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
User = get_user_model()

from blogs.forms import PostForm, NewPostForm

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

def post_detail(request):
    """Post detail view."""
    return render(request, 'home.html')
