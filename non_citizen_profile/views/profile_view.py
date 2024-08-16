from rest_framework import viewsets
from ..models import Address, Biometrics, ContactDetails, Passport, PersonalDetails
from api.serializers import AddressSerializer, BiometricsSerializer, ContactDetailsSerializer, PassportSerializer, PersonalDetailsSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class BiometricsViewSet(viewsets.ModelViewSet):
    queryset = Biometrics.objects.all()
    serializer_class = BiometricsSerializer

class ContactDetailsViewSet(viewsets.ModelViewSet):
    queryset = ContactDetails.objects.all()
    serializer_class = ContactDetailsSerializer

class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer

class PersonalDetailsViewSet(viewsets.ModelViewSet):
    queryset = PersonalDetails.objects.all()
    serializer_class = PersonalDetailsSerializer