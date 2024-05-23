from rest_framework import viewsets
from ..models import Under20Citizenship
from lichois.citizenship.api.serializers import Under20CitizenshipSerializer


class Under20CitizenshipViewSet(viewsets.ModelViewSet):
    queryset = Under20Citizenship.objects.all()
    serializer_class = Under20CitizenshipSerializer
