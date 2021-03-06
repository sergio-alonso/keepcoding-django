"""Django blogs urls."""
from django.conf.urls import include, url

from blogs import views

urlpatterns = [
    url(r'^(?P<user_email>[\w.@+-]+)/post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^(?P<user_email>[\w.@+-]+)/$', views.blog, name='blog'),
    url(r'post-save', views.post_save, name='post_save'),
    url(r'^$', views.BlogsListView.as_view(), name='blogs_list'),
]
