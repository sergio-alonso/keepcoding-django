"""Django blogs urls."""
from django.conf.urls import url

from blogs import views

urlpatterns = [
    url(r'^(?P<user_email>[\w.@+-]+)/$', views.blog, name='blog'),
]
