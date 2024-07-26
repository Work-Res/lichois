import django_filters

from rest_framework import viewsets
from rest_framework.response import Response

from ..api.serializers import AssessmentResultSerializer, AssessmentSerializer
from ..models import Assessment
from ..models.assessment_result import AssessmentResult


class AssessmentResultModelFilter(django_filters.FilterSet):

    document_number = django_filters.CharFilter(
        field_name="document_number", lookup_expr="exact"
    )

    min_result_date = django_filters.DateFilter(field_name="created", lookup_expr="gte")
    max_result_date = django_filters.DateFilter(field_name="created", lookup_expr="lte")

    class Meta:
        model = AssessmentResult
        exclude = ("user_created", "output_results")
        fields = "__all__"


class AssessmentModelFilter(django_filters.FilterSet):

    document_number = django_filters.CharFilter(
        document_number="document_number", lookup_expr="exact"
    )

    min_result_date = django_filters.DateFilter(field_name="created", lookup_expr="gte")
    max_result_date = django_filters.DateFilter(field_name="created", lookup_expr="lte")

    class Meta:
        model = Assessment
        exclude = ("user_created", "marking_score")


class AssessmentResultViewSet(viewsets.ModelViewSet):
    lookup_field = "document_number"
    queryset = AssessmentResult.objects.all()
    serializer_class = AssessmentResultSerializer
    filterset_class = AssessmentResultModelFilter


class AssessmentViewSet(viewsets.ModelViewSet):
    lookup_field = "document_number"
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    filterset_class = AssessmentModelFilter

    def retrieve(self, request, document_number, *args, **kwargs):
        assessment = Assessment.objects.filter(document_number=document_number)
        serializer = AssessmentSerializer(assessment, many=True)
        return Response(serializer.data)
