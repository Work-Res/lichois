from rest_framework import viewsets
from ..models import CommitalWarrent, NonCitizen, PIDeclarationOrderAcknowledgement, PIDeclarationOrder, PIRecommendation, Prisoner, PrisonerDueRelease
from api.serializers import CommitalWarrentSerializer, NonCitizenSerializer, PIDeclarationOrderAcknowledgementSerializer, PIDeclarationOrderSerializer, PIRecommendationSerializer, PrisonerSerializer, PrisonerDueReleaseSerializer


class CommitalWarrentViewSet(viewsets.ModelViewSet):
    queryset = CommitalWarrent.objects.all()
    serializer_class = CommitalWarrentSerializer


class NonCitizenViewSet(viewsets.ModelViewSet):
    queryset = NonCitizen.objects.all()
    serializer_class = NonCitizenSerializer

class PIDeclarationOrderAcknowledgementViewSet(viewsets.ModelViewSet):
    queryset = PIDeclarationOrderAcknowledgement.objects.all()
    serializer_class = PIDeclarationOrderAcknowledgementSerializer

class PIDeclarationOrderViewSet(viewsets.ModelViewSet):
    queryset = PIDeclarationOrder.objects.all()
    serializer_class = PIDeclarationOrderSerializer


class PIRecommendationViewSet(viewsets.ModelViewSet):
    queryset = PIRecommendation.objects.all()
    serializer_class = PIRecommendationSerializer

class PrisonerViewSet(viewsets.ModelViewSet):
    queryset = Prisoner.objects.all()
    serializer_class = PrisonerSerializer

class PrisonerDueReleaseViewSet(viewsets.ModelViewSet):
    queryset = PrisonerDueRelease.objects.all()
    serializer_class = PrisonerDueReleaseSerializer