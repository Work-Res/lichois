from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.classes.application_summary import ApplicationSummary
from ..models import PermitReplacement
from ..api.serializers import PermitReplacementSerializer


def get_app_labels():
    return [
        "workresidentpermit.PermitReplacement",
        "workresidentpermit.CommissionerDecision",
        "workresidentpermit.MinisterDecision",
    ]


class PermitReplacementViewSet(viewsets.ModelViewSet):
    queryset = PermitReplacement.objects.all()
    serializer_class = PermitReplacementSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="summary/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="replacement-permit-summary",
    )
    def summary(self, request, document_number):
        app_summary = ApplicationSummary(document_number, get_app_labels())
        return Response(data=app_summary.data())
