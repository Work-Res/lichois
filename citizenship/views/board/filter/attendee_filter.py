import django_filters

from citizenship.models import Attendee


class AttendeeFilter(django_filters.FilterSet):
    class Meta:
        model = Attendee
        fields = {
            'meeting': ['exact'],
            'member': ['exact'],
            'confirmed': ['exact'],
            'proposed_date': ['exact', 'lt', 'gt'],
        }
