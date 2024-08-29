from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..classes import NonCitizenProfileDeserializer


class CreateNonCitizenProfileView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs) -> Response:
        response = NonCitizenProfileDeserializer(request.data)
        errors = response.handle()
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data={"message": "Successfully created non citizen profile"},
            status=status.HTTP_201_CREATED,
        )
