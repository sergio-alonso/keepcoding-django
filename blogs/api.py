from rest_framework import routers

from blogs.viewsets import UserViewSet, BlogsViewSet, PostViewSet

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)
router.register(r'blogs', BlogsViewSet, 'blogs')
router.register(r'blogs/(?P<email>[\w.@+-]+)/post', PostViewSet)
