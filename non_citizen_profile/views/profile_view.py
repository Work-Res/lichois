from rest_framework import viewsets
from ..models import (
    Address,
    Biometrics,
    ContactDetails,
    Passport,
    PersonalDetails,
    Education,
    NextOfKin,
)
from ..api.serializers import (
    AddressSerializer,
    BiometricsSerializer,
    ContactDetailsSerializer,
    PassportSerializer,
    PersonalDetailsSerializer,
    EducationSerializer,
    NextOfKinSerializer,
)


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


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class NextOfKinViewSet(viewsets.ModelViewSet):
    queryset = NextOfKin.objects.all()
    serializer_class = NextOfKinSerializer
