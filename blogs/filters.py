import django_filters

from blogs.models import Post


class CategoryFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(name="category")

    class Meta:
        model = Post
        fields = ['category']
