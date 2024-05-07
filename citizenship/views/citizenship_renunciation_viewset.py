from rest_framework import viewsets
from ..models import RenunciationOfCitizenship
from ..serializers import RenunciationOfCitizenshipSerializer


class RenunciationOfCitizenshipViewSet(viewsets.ModelViewSet):
    queryset = RenunciationOfCitizenship.objects.all()
    serializer_class = RenunciationOfCitizenshipSerializer
