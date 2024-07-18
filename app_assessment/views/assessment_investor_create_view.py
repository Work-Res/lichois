import django_filters

from rest_framework import viewsets
from rest_framework.response import Response

from ..api.serializers import AssessmentInvestorSerializer
from ..models import Assessment, AssessmentInvestor


class AssessmentInvestorModelFilter(django_filters.FilterSet):
	document_number = django_filters.CharFilter(
		field_name='document_number', lookup_expr='exact')
	
	min_result_date = django_filters.DateFilter(field_name='created', lookup_expr='gte')
	max_result_date = django_filters.DateFilter(field_name='created', lookup_expr='lte')
	
	class Meta:
		model = AssessmentInvestor
		exclude = ('user_created', 'marking_score')
		fields = '__all__'


class AssessmentInvestorViewSet(viewsets.ModelViewSet):
	lookup_field = 'document_number'
	queryset = AssessmentInvestor.objects.all()
	serializer_class = AssessmentInvestorSerializer
	filterset_class = AssessmentInvestorModelFilter
	
	def retrieve(self, request, document_number=None, *args, **kwargs):
		assessment = AssessmentInvestor.objects.filter(document_number=document_number)
		serializer = AssessmentInvestorSerializer(assessment, many=True)
		return Response(serializer.data)