from rest_framework import viewsets
from ..models import InterestDeclaration
from ..serializers import InterestDeclarationSerializer


class InterestDeclarationViewSet(viewsets.ModelViewSet):
	queryset = InterestDeclaration.objects.all()
	serializer_class = InterestDeclarationSerializer
