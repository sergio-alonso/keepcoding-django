from django.contrib import admin

from blogs.models import Category, Post

admin.site.register(Category)
admin.site.register(Post)
