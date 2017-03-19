"""Django blogs urls."""
from django.conf.urls import url

from blogs import views

urlpatterns = [
    url(r'^(?P<user_email>[\w.@+-]+)/(?P<post_id>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<user_email>[\w.@+-]+)/$', views.blog, name='blog'),
    url(r'post-save', views.post_save, name='post_save'),
]
