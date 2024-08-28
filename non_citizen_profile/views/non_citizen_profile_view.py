from ..api.serializers import CombinedSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..classes import NonCitizenProfile, NonCitizenProfileDeserializer


class NonCitizenProfileView(APIView):
    def get(self, request, non_citizen_identifier, *args, **kwargs):
        profile = NonCitizenProfile(non_citizen_identifier)
        serializer = CombinedSerializer(profile.get_combined_profile())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> Response:
        response = NonCitizenProfileDeserializer(request.data)
        errors = response.handle()
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data={"message": "Successfully created non citizen profile"},
            status=status.HTTP_201_CREATED,
        )
