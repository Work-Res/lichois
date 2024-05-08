from rest_framework import viewsets
from ..models import NationalityDeclaration
from ..serializers import NationalityDeclarationSerializer


class NationalityDeclarationViewSet(viewsets.ModelViewSet):
    queryset = NationalityDeclaration.objects.all()
    serializer_class = NationalityDeclarationSerializer
