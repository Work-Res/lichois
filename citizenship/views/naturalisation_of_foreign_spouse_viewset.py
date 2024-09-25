from rest_framework import viewsets
# from models import NaturalisationOfForeignSpouse
# from lichois.citizenship.api.serializers import NaturalisationOfForeignSpouseSerializer


class NaturalisationOfForeignSpouseViewSet(viewsets.ModelViewSet):
    queryset = NaturalisationOfForeignSpouse.objects.all()
    serializer_class = NaturalisationOfForeignSpouseSerializer
