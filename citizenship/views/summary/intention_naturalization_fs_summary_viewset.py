from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.classes.application_summary import ApplicationSummary


def get_app_labels():
    return [
        
        # residential_history,
        "citizenship.ResidentialHistory"
        # oath
        "citizenship.OathOfAllegiance"
        # model
        "citizenship.DeclarationNaturalisationByForeignSpouse",
    ]


class IntentionNaturalizationFSSummaryViewSet(viewsets.ModelViewSet):


    @action(
        detail=False,
        methods=["get"],
        url_path="summary/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="intention-fs-summary",
    )
    def summary(self, request, document_number):
        app_summary = ApplicationSummary(document_number, get_app_labels())
        return Response(data=app_summary.data())
