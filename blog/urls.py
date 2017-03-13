"""Django blog urls."""
from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^new$', views.new_blog, name='new-blog'),
    url(r'^(\d+)/$', views.list_posts, name='list-posts'),
]
