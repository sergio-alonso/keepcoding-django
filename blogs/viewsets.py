from rest_framework import viewsets, filters, status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from django.utils.timezone import now
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
User = get_user_model()

from blogs.filters import CategoryFilter
from blogs.permissions import IsAnonCreate, IsOwnerOrAdmin, IsOwnerOrReadOnly
from blogs.serializers import UserSerializer, BlogsSerializer, PostSerializer
from blogs.models import Post

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
    queryset = User.objects.annotate(posts_count=Count('post')).all().order_by('email')
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
