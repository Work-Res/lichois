from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.classes.application_summary import ApplicationSummary


def get_app_labels():
    return [
        # "citizenship.CertificateOfOrigin",
        # "citizenship.RenunciationOfCitizenship",
        # "app_oath.Declarant"
    ]


class PresPower10BSummaryViewSet(viewsets.ModelViewSet):


    @action(
        detail=False,
        methods=["get"],
        url_path="summary/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="pres-power-10B-summary",
    )
    def summary(self, request, document_number):
        app_summary = ApplicationSummary(document_number, get_app_labels())
        return Response(data=app_summary.data())