from django.db.models import Q
from django_filters import rest_framework as filters

from app.posts.models import Posts


class PostFilter(filters.FilterSet):
    colors = filters.CharFilter(method='filter_colors')

    class Meta:
        model = Posts
        fields = [
            'colors',
        ]

    def filter_colors(self, queryset, name, value):
        """
        , separated Filter
        """
        filter_object = Q()

        for color in value.split():
            filter_object |= Q(colors__type=color)

        return queryset.filter(filter_object)
