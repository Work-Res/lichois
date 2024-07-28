from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.classes.application_summary import ApplicationSummary

from ...models import BlueCard
from ..serializers import BlueCardSerializer


def get_app_labels():
    return [
        "app_personal_details.NextOfKin",
        "app.MinisterDecision",
        "app.SecurityClearance",
    ]


class BlueCardViewSet(viewsets.ModelViewSet):
    queryset = BlueCard.objects.all()
    serializer_class = BlueCardSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="summary/(?P<document_number>[A-Za-z0-9-]+)",
        url_name="blue-card-summary",
    )
    def summary(self, request, document_number):
        app_summary = ApplicationSummary(document_number, get_app_labels())
        return Response(data=app_summary.data())
