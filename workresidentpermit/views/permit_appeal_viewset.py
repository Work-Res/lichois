from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.classes.application_summary import ApplicationSummary
from ..models import PermitAppeal
from ..api.serializers import PermitAppealSerializer


def get_app_labels():
    return [
        'workresidentpermit.PermitAppeal'
    ]


class PermitAppealViewSet(viewsets.ModelViewSet):
    queryset = PermitAppeal.objects.all()
    serializer_class = PermitAppealSerializer

    @action(detail=False, methods=['get'], url_path='summary/(?P<document_number>[A-Za-z0-9-]+)',
            url_name='resident-appeal-summary')
    def summary(self, request, document_number):
        app_summary = ApplicationSummary(document_number, get_app_labels())
        return Response(data=app_summary.data())
