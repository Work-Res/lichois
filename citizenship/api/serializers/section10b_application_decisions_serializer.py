from rest_framework import serializers

from app.api.serializers import ApplicationSerializer
from citizenship.models import Section10bApplicationDecisions


class Section10bApplicationDecisionsSerializer(serializers.ModelSerializer):
    """Serializer for Section10bApplicationDecisions."""

    application = ApplicationSerializer(read_only=True)  # Nested application data

    class Meta:
        model = Section10bApplicationDecisions
        fields = [
            'id',
            'application',
            'mlha_director_decision',
            'deputy_permanent_secretary',
            'permanent_secretary',
            'pres_permanent_secretary',
            'president_decision',
        ]
