from rest_framework import viewsets
from ..models import PresidentialDeclaration, MovementLog, Interaction
from api.serializers import PresidentialDeclarationSerializer, MovementLogSerializer, InteractionSerializer, TracingInformationSerializer


class PresidentialDeclarationViewSet(viewsets.ModelViewSet):
    queryset = PresidentialDeclaration.objects.all()
    serializer_class = PresidentialDeclarationSerializer


class MovementLogViewSet(viewsets.ModelViewSet):
    queryset = MovementLog.objects.all()
    serializer_class = MovementLogSerializer

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

class TracingInformationViewSet(viewsets.ViewSet):
    def list(self, request):
        presidential_declaration = PresidentialDeclaration.objects.first()
        movement_log = MovementLog.objects.first()
        interaction = Interaction.objects.first()

        data = {
            "presidential_declaration": PresidentialDeclarationSerializer(presidential_declaration).data if presidential_declaration else None,
            "movement_log": MovementLogSerializer(movement_log).data if movement_log else None,
            "interaction": InteractionSerializer(interaction).data if interaction else None,
        }

        serializer = TracingInformationSerializer(data)
        return Response(serializer.data)