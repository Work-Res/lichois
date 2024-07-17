import django_filters

from app_personal_details.models import Person
from workresidentpermit.choices import PERSON_TYPE


class PersonFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    middle_name = django_filters.CharFilter(lookup_expr='icontains')
    maiden_name = django_filters.CharFilter(lookup_expr='icontains')
    dob = django_filters.DateFilter()
    country_birth = django_filters.CharFilter(lookup_expr='icontains')
    place_birth = django_filters.CharFilter(lookup_expr='icontains')
    occupation = django_filters.CharFilter(lookup_expr='icontains')
    qualification = django_filters.CharFilter(lookup_expr='icontains')
    person_type = django_filters.ChoiceFilter(choices=PERSON_TYPE)

    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'maiden_name',
            'marital_status',
            'dob',
            'country_birth',
            'place_birth',
            'gender',
            'occupation',
            'qualification',
            'person_type'
        ]
