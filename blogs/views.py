from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def blog(request, user_email):
    return render(request, 'blog.html')
