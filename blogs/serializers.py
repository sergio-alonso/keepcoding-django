from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()

from blogs.forms import EMPTY_POST_TITLE_ERROR, DUPLICATE_POST_TITLE_ERROR
from blogs.models import Post

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        allow_blank=False,
        error_messages={'blank': EMPTY_POST_TITLE_ERROR},
    )
    author = serializers.CharField(
        source='get_author',
        read_only=True
    )

    class Meta:
        model = Post
        fields = ('title','imagen', 'summary', 'published_date', 'author')

class BlogsSerializer(serializers.ModelSerializer):
    blog = serializers.CharField(source='get_blog_url')
    posts_count = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('blog', 'posts_count')

class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True, many=True, source='post_set')

    class Meta:
        model = User
        fields = ('email', 'password', 'posts', 'is_admin')
