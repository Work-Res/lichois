from requests import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from app.classes.application_summary import ApplicationSummary

from ...models import VisaApplication
from ..serializers import VisaApplicationSerializer


def get_app_labels():
    return [
        "visa.VisaApplication",
    ]


class VisaApplicationViewSet(viewsets.ModelViewSet):
    queryset = VisaApplication.objects.all()
    serializer_class = VisaApplicationSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="summary/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="visa-summary",
    )
    def summary(self, request, document_number):
        app_summary = ApplicationSummary(document_number, get_app_labels())
        return Response(data=app_summary.data())
