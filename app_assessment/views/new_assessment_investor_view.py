import django_filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..api.serializers import NewAssessmentInvestorSerializer
from ..models import NewAssessmentInvestor


class NewAssessmentInvestorModelFilter(django_filters.FilterSet):
    document_number = django_filters.CharFilter(
        field_name="document_number", lookup_expr="exact"
    )

    min_result_date = django_filters.DateFilter(field_name="created", lookup_expr="gte")
    max_result_date = django_filters.DateFilter(field_name="created", lookup_expr="lte")

    class Meta:
        model = NewAssessmentInvestor
        exclude = ("user_created", "marking_score")
        fields = "__all__"


class NewAssessmentInvestorViewSet(viewsets.ModelViewSet):
    lookup_field = "document_number"
    queryset = NewAssessmentInvestor.objects.all()
    serializer_class = NewAssessmentInvestorSerializer
    filterset_class = NewAssessmentInvestorModelFilter

    def retrieve(self, request, document_number=None, *args, **kwargs):
        assessment = NewAssessmentInvestor.objects.filter(
            document_number=document_number
        )
        serializer = NewAssessmentInvestorSerializer(assessment, many=True)
        return Response(serializer.data)
