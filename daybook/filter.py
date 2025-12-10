import django_filters

class EntriesFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name='text', lookup_expr='icontains')

