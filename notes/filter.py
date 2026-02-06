import django_filters
from django.db.models import Q


class SectionTopicFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(sections__title__icontains=value) |
            Q(sections__description__icontains=value)
        ).distinct()


class SectionFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value)
        ).distinct()