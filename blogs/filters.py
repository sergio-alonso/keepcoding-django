from rest_framework import filters

from blogs.models import Post

class CategoryFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get('category', None)
        if category:
            category = category.split(',')
            queryset = queryset.filter(category__name__in=category).distinct()

        return queryset
