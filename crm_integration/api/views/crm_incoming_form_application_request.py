from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class CrmIncomingFormApplicationRequest(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        # Retrieve the data from the request
        data = request.data
        
        # Process the data (You can add your custom logic here)
        print(data)
        
        # Return the processed data as a response
        return Response({'processed_data': "processed_data coli"}, status=status.HTTP_200_OK)