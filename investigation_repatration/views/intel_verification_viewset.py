from rest_framework import viewsets
from ..models import IntelVerification
from api.serializers import IntelVerificationSerializer


class IntelVerificationViewSet(viewsets.ModelViewSet):
    queryset = IntelVerification.objects.all()
    serializer_class = IntelVerificationSerializer
