from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def my_blog(request, user_email):
    return render(request, 'home.html')
