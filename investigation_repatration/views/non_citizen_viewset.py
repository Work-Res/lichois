from rest_framework import viewsets
from ..models import NonCitizen
from api.serializers import NonCitizenSerializer


class NonCitizenViewSet(viewsets.ModelViewSet):
    queryset = NonCitizen.objects.all()
    serializer_class = NonCitizenSerializer
