import django_filters

from app_information_requests.models import InformationMissingRequest


class InformationMissingRequestFilter(django_filters.FilterSet):
    class Meta:
        model = InformationMissingRequest
        fields = {
            'parent_object_id': ['exact', 'icontains'],
            'parent_type': ['exact', 'icontains'],
            'information_request': ['exact'],
            'reason': ['exact', 'icontains'],
            'description': ['icontains'],
            'is_provided': ['exact'],
        }
