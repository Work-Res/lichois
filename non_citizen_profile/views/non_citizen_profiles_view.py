from ..api.serializers import CombinedSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..classes import NonCitizenProfile


class NonCitizenProfilesView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        first_name = request.query_params.get("first_name")
        last_name = request.query_params.get("last_name")
        permit_number = request.query_params.get("permit_number")
        non_citizen_identifier = request.query_params.get("non_citizen_identifier")
        profile = NonCitizenProfile(
            first_name=first_name,
            last_name=last_name,
            permit_number=permit_number,
            identifier=non_citizen_identifier,
        )

        data = profile.get_all_profiles()
        return Response(data, status=status.HTTP_200_OK)
