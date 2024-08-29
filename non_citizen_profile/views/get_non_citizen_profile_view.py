from ..api.serializers import CombinedSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..classes import NonCitizenProfile


class GetNonCitizenProfileView(APIView):
    def get(self, request, non_citizen_identifier, *args, **kwargs) -> Response:
        profile = NonCitizenProfile(identifier=non_citizen_identifier)
        data = profile.get_combined_profile()
        return Response(data, status=status.HTTP_200_OK)
