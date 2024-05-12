from rest_framework import viewsets
from ..models import ContactMethod
from ..serializers import ContactMethodSerializer


class ContactMethodViewSet(viewsets.ModelViewSet):
    queryset = ContactMethod.objects.all()
    serializer_class = ContactMethodSerializer