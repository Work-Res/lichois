import django_filters
from django_filters import rest_framework as filters

from citizenship.models import OathOfAllegiance


class OathOfAllegianceFilter(django_filters.FilterSet):

    declaration_fname = filters.CharFilter(lookup_expr='icontains')
    declaration_lname = filters.CharFilter(lookup_expr='icontains')
    declaration_date = filters.DateFilter()
    signature = filters.CharFilter(lookup_expr='icontains')
    document_number = filters.CharFilter(field_name='document_number', lookup_expr='exact')

    class Meta:
        model = OathOfAllegiance
        fields = ['declaration_fname', 'declaration_lname', 'declaration_date', 'signature']
