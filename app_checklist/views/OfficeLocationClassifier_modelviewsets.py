# app_checklist/views.py
from rest_framework import viewsets
from app_checklist.models import OfficeLocationClassifier
from app_checklist.serializers import OfficeLocationClassifierSerializer

class OfficeLocationClassifierViewSet(viewsets.ModelViewSet):
    queryset = OfficeLocationClassifier.objects.all()
    serializer_class = OfficeLocationClassifierSerializer

