from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.classes.application_summary import ApplicationSummary
from citizenship.api.serializers import CitizenshipSummarySerializer
from citizenship.models import CitizenshipSummary
from django.http import JsonResponse


def get_app_labels():
    return [
        "citizenship.DeclarationNaturalisationByForeignSpouse",
    ]


class IntentionNaturalizationFSSummaryViewSet(viewsets.ModelViewSet):

    queryset = CitizenshipSummary.objects.all()
    serializer_class = CitizenshipSummarySerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="summary/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="intention-fs-summary",
    )
    def summary(self, request, document_number):
        app_summary = ApplicationSummary(document_number, get_app_labels())
        return JsonResponse(data=app_summary.data())
