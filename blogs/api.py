from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueTogetherValidator

from blogs.models import Post
from blogs.forms import EMPTY_POST_TITLE_ERROR, DUPLICATE_POST_TITLE_ERROR

from django.contrib.auth import get_user_model
User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        allow_blank=False, error_messages={'blank': EMPTY_POST_TITLE_ERROR}
    )

    class Meta:
        model = Post
        fields = ('id', 'owner', 'title')
        validators = [
            UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=('owner', 'title'),
                message=DUPLICATE_POST_TITLE_ERROR
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, source='post_set')

    class Meta:
        model = User
        fields = ('email', 'posts',)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '[\w.@+-]+'
    queryset = User.objects.all()
    serializer_class = UserSerializer

router = routers.SimpleRouter()
router.register(r'post', PostViewSet)
router.register(r'user', UserViewSet)
