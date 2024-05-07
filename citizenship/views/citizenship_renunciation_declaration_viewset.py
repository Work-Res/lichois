from rest_framework import viewsets
from ..models import CitizenshipRenunciationDeclaration
from ..serializers import CitizenshipRenunciationDeclarationSerializer


class CitizenshipRenunciationDeclarationViewSet(viewsets.ModelViewSet):
    queryset = CitizenshipRenunciationDeclaration.objects.all()
    serializer_class = CitizenshipRenunciationDeclarationSerializer
