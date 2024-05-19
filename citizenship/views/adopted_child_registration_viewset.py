from rest_framework import viewsets
from ..models import AdoptedChildRegistration
from lichois.citizenship.api.serializers import AdoptedChildRegistrationSerializer


class AdoptedChildRegistrationViewSet(viewsets.ModelViewSet):
    queryset = AdoptedChildRegistration.objects.all()
    serializer_class = AdoptedChildRegistrationSerializer
