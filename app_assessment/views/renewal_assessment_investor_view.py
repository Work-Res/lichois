import django_filters
from rest_framework import viewsets
from rest_framework.response import Response

from ..api.serializers import RenewalAssessmentInvestorSerializer
from ..models import RenewalAssessmentInvestor


class RenewalAssessmentInvestorModelFilter(django_filters.FilterSet):
    document_number = django_filters.CharFilter(
        field_name="document_number", lookup_expr="exact"
    )

    min_result_date = django_filters.DateFilter(field_name="created", lookup_expr="gte")
    max_result_date = django_filters.DateFilter(field_name="created", lookup_expr="lte")

    class Meta:
        model = RenewalAssessmentInvestor
        exclude = ("user_created", "marking_score")
        fields = "__all__"


class RenewalAssessmentInvestorViewSet(viewsets.ModelViewSet):
    lookup_field = "document_number"
    queryset = RenewalAssessmentInvestor.objects.all()
    serializer_class = RenewalAssessmentInvestorSerializer
    filterset_class = RenewalAssessmentInvestorModelFilter

    def retrieve(self, request, document_number=None, *args, **kwargs):
        assessment = RenewalAssessmentInvestor.objects.filter(
            document_number=document_number
        )
        serializer = RenewalAssessmentInvestorSerializer(assessment, many=True)
        return Response(serializer.data)
