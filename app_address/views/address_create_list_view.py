from rest_framework import viewsets

from ..models import ApplicationAddress
from ..api.serializers import ApplicationAddressSerializer


class AddressCreateListView(viewsets.ModelViewSet):
    queryset = ApplicationAddress.objects.all()
    serializer_class = ApplicationAddressSerializer
