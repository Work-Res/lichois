from rest_framework.views import APIView

from .base_crm_api_view import BaseCrmAPIView



class ExemptionCrmAPIView(BaseCrmAPIView, APIView):

    def create_application(self):
        """
        """
        
        # Todo: override the method in process application specific data 
        pass