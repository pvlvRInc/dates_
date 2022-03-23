import django_filters

from date.models import User


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='startswith')
    last_name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender']
