from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from app.classes.application_summary import ApplicationSummary

from ...models import PermanentResidence
from ..serializers import PermanentResidenceSerializer


def get_app_labels():
    return [
        "permanent_residence.PermanentResidence",
        "app.CommissionerDecision",
    ]


class PermanentResidenceViewSet(viewsets.ModelViewSet):
    queryset = PermanentResidence.objects.all()
    serializer_class = PermanentResidenceSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="summary/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="permanent-residence-summary",
    )
    def summary(self, request, document_number):
        app_summary = ApplicationSummary(document_number, get_app_labels())
        return Response(data=app_summary.data())
