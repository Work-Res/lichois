from rest_framework import serializers
from ...models import PresidentialDeclaration, MovementLog, Interaction

class PresidentialDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresidentialDeclaration
        fields = '__all__'

class MovementLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementLog
        fields = '__all__'

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'

class TracingInformationSerializer(serializers.Serializer):
    presidential_declaration = PresidentialDeclarationSerializer()
    movement_log = MovementLogSerializer()
    interaction = InteractionSerializer()