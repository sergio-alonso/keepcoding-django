"""keepcoding_django URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url

from accounts import urls as accounts_urls
from blogs import urls as blogs_urls

from blogs import views as blogs_views

urlpatterns = [
    url(r'^$', blogs_views.home, name='home'),
    url(r'^new-post$', blogs_views.post_create , name='post_create'),
    url(r'^blogs/', include(blogs_urls)),
    url(r'^accounts/', include(accounts_urls)),
]
