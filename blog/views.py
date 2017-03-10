"""Django blog app views."""
from django.shortcuts import render


def home_page(request):
    """Home page view."""
    return render(request, 'home.html')
