from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ...classes import CrmRequestHandler



class BaseCrmAPIView(APIView):

    permission_classes = [AllowAny]
    

    def get(self, request):
        return Response({'processed_data': "processed_data get method called here"}, status=status.HTTP_200_OK)

    def post(self, request):
        # Retrieve the data from the request
        data = self.build_master_dict(request)
        print(data)
        # Process the data (You can add your custom logic here)
        self.process_data(build_master_dict=data)
        
        # Return the processed data as a response
        return Response({'processed_data': "processed_data coli"}, status=status.HTTP_200_OK)

    def process_data(self, build_master_dict=None):
        """Extract form data and create or update instances.
        """
        crm_request = CrmRequestHandler(
            crm_request=build_master_dict)

        return crm_request.group_and_trim_keys()
    
    def build_master_dict(self, request):
        """Build and return master form data dictionary.
        """
        payload = request.data["payload"]
        form_data = payload["form"]
        
        # Input data
        data = list(form_data.values())
        merged_data_dict = {}
        
        for d in data:
            merged_data_dict.update(d)
        return merged_data_dict


    def create_application(self):
        """
        """
        
        # Todo: override the method in process application specific data 
        pass