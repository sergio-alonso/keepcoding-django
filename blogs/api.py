from rest_framework import status
from rest_framework import routers, serializers, viewsets, generics, filters, renderers, mixins
from rest_framework.validators import UniqueValidator
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import now

from blogs.models import Post
from blogs.forms import EMPTY_POST_TITLE_ERROR, DUPLICATE_POST_TITLE_ERROR
from blogs.filters import CategoryFilter

from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import permissions

class IsAnonCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and not request.user.is_authenticated:
            return True
        elif request.method == "PATCH" and request.user.is_authenticated:
            return True
        elif request.method == "DELETE" and request.user.is_authenticated:
            return True
        elif request.method != "POST" and not request.user.is_authenticated:
            return False
        elif request.method in permissions.SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.email == request.user.email or request.user.is_admin

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user or request.user.is_admin

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_admin


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        allow_blank=False,
        error_messages={'blank': EMPTY_POST_TITLE_ERROR},
    )

    class Meta:
        model = Post
        fields = ('title','imagen', 'summary', 'published_date',)

class BlogsSerializer(serializers.ModelSerializer):
    blog = serializers.CharField(source='get_blog_url')

    class Meta:
        model = User
        fields = ('blog',)

class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True, many=True, source='post_set')

    class Meta:
        model = User
        fields = ('email', 'password', 'posts', 'is_admin')


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsOwnerOrAdmin, IsAnonCreate))
class UserViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '[\w.@+-]+'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return User.objects.all()
        else:
            return User.objects.filter(email=self.request.user.email)

class BlogsViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_value_regex = '[\w.@+-]+'
    queryset = User.objects.all().order_by('email')
    serializer_class = BlogsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email',)

@permission_classes((IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly,))
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('owner').all().order_by('-published_date')
    serializer_class = PostSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    search_fields = ('title', 'summary',)
    filter_class = CategoryFilter
    ordering = ('title', 'published_date',)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.filter(Q(published_date__lte=now()))
        elif self.request.user.is_admin:
            return self.queryset.all()
        else:
            return self.queryset.filter(Q(owner=self.request.user.email) | Q(published_date__lte=now()))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, published_date=now())
        return serializer

    def create(self, request, *args, **kwargs):

        if kwargs['email'] != self.request.user.email:
            # user is not the blog owner
            return Response(data={'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)
router.register(r'blogs', BlogsViewSet, 'blogs')
router.register(r'blogs/(?P<email>[\w.@+-]+)/post', PostViewSet)
