from rest_framework import viewsets
from ..models import RenunciationOfForeignCitizenship
from ..serializers import RenunciationOfForeignCitizenshipSerializer


class RenunciationOfForeignCitizenshipViewSet(viewsets.ModelViewSet):
    queryset = RenunciationOfForeignCitizenship.objects.all()
    serializer_class = RenunciationOfForeignCitizenshipSerializer
