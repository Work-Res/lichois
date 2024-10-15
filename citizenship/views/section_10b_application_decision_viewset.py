from rest_framework import viewsets


from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.section10b_application_decisions_serializer import \
    Section10bApplicationDecisionsSerializer
from citizenship.models import Section10bApplicationDecisions
from citizenship.views.filters.section10b_application_decisions_filter import Section10bApplicationDecisionsFilter


class Section10bApplicationDecisionsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Section 10B Application Decisions instances.
    """
    queryset = Section10bApplicationDecisions.objects.all()
    serializer_class = Section10bApplicationDecisionsSerializer
    filterset_class = Section10bApplicationDecisionsFilter
    pagination_class = StandardResultsSetPagination
