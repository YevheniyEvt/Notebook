import django_filters
from django.db.models import Q

from agent.models import Chat


class ChatFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Chat
        fields = ['name']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )