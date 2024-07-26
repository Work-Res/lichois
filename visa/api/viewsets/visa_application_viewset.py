from rest_framework import viewsets

from ..serializers import VisaApplicationSerializer
from ...models import VisaApplication


class VisaApplicationViewSet(viewsets.ModelViewSet):
    queryset = VisaApplication.objects.all()
    serializer_class = VisaApplicationSerializer
