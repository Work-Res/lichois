from django_filters import rest_framework as filters
from .models import SystemParameter

class SystemParameterFilter(filters.FilterSet):
    document_number = filters.CharFilter(field_name='document_number', lookup_expr='in')

    class Meta:
        model = SystemParameter
        fields = '__all__'  
