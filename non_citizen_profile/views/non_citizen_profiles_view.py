from ..api.serializers import CombinedSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..classes import NonCitizenProfile


class NonCitizenProfilesView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        profile = NonCitizenProfile()
        data = profile.get_all_profiles()
        return Response(data, status=status.HTTP_200_OK)
