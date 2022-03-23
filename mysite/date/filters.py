from math import *

import django_filters

from date.models import User


class UserFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.user_name = kwargs.pop('request', None).user

        queryset = kwargs.pop('queryset')
        self.current_user = queryset.get(username=self.user_name)
        queryset = queryset.exclude(pk=self.current_user.pk)

        super(UserFilter, self).__init__(*args, **kwargs, queryset=queryset)

    first_name = django_filters.CharFilter(lookup_expr='startswith')
    last_name = django_filters.CharFilter(lookup_expr='startswith')
    distance = django_filters.RangeFilter(label='Distance', method='distance_filter')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'distance']

    def distance_filter(self, queryset, name, value):
        if self.user_name != 'AnonymousUser':
            earth_radius = 6371.009
            exclude_pks = []
            for some_user in queryset:
                lng1, lat1, lng2, lat2 = map(radians, (self.current_user.longitude, self.current_user.latitude,
                                                       some_user.longitude, some_user.latitude))
                d_lon = lng2 - lng1
                d_lat = lat2 - lat1
                central_angle = 2 * asin(sqrt(sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2))
                distance = earth_radius * central_angle

                if value.start and value.stop and (distance < value.start or value.stop <= distance):
                    exclude_pks.append(some_user.pk)
                elif value.start and distance < value.start:
                    exclude_pks.append(some_user.pk)
                elif value.stop and value.stop <= distance:
                    exclude_pks.append(some_user.pk)
        return queryset.exclude(pk__in=exclude_pks)
