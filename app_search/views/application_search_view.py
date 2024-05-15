from drf_haystack.serializers import HaystackSerializer
from drf_haystack.viewsets import HaystackViewSet

from app.models import ApplicationVersion

from app.api.serializers import ApplicationVersionSerializer

from ..search_indexes import ApplicationVersionIndex


class ApplicationSearchSerializer(HaystackSerializer):

    class Meta:
        index_classes = [ApplicationVersionIndex]

        fields = [
            "document_number", "application_type", "submission_date", "application_status", "full_name",
            "user_identifier", "verification_status", "security_clearance_status", "board_decision", "status"
        ]


class ApplicationVersionSearchView(HaystackViewSet):

    index_models = [ApplicationVersion]

    serializer_class = ApplicationVersionSerializer
