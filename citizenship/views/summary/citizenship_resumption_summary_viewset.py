from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.classes.application_summary import ApplicationSummary


def get_app_labels():
    return [
        # personal_info,
        # address_info,
        # contact_info,
        # parental_details_father,
        # parental_details_mother
    ]


class CitizenshipResumptionSummaryViewSet(viewsets.ModelViewSet):


    @action(
        detail=False,
        methods=["get"],
        url_path="summary/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="citizenship-resumption-summary",
    )
    def summary(self, request, document_number):
        app_summary = ApplicationSummary(document_number, get_app_labels())
        return Response(data=app_summary.data())
