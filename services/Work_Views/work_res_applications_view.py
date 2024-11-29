from django.views.generic import TemplateView

from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from app_personal_details.models import (
    Person, Passport, Education, ParentalDetails,
    NextOfKin, Spouse, Child)
from workresidentpermit.models import ResidencePermit, WorkPermit


from ..classes import WorkResApplicationForms


class WorkPermitDashboardView(TemplateView):
    template_name = 'applications/work-res/work-res-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        
    
        context.update(
            application_number=self.application_number(),
            new_application=self.new_application,
            create_new_application=self.create_new_application,
            application_forms= self.application_forms
            )

        return context

    @property
    def application_forms(self):
        """Returns application forms and urls.
        """
        model_cls_list = [
            Person, ApplicationAddress, Country,
            ApplicationContact, Passport, Education,
            NextOfKin, ParentalDetails, Spouse,
            Child, WorkPermit, ResidencePermit] # This could come from a config file
    
        forms_urls = WorkResApplicationForms(
            application_number=self.application_number(),
            application_models_cls=model_cls_list).application_urls()
        print(forms_urls, '###############')
        return forms_urls

    def application_number(self):
        """Returns an application number.
        """
        application_number = '12345' #self.request.GET.get('application_number', '')
        
        #Impliment this method to get a permit application number for a permit being applied for.
        
        return application_number


    def permits(self):
        """Returns a list of all work and res permits.
        """
        return None
    
    @property
    def new_application(self):
        """Return true if a new application is in progress.
        """
        return True

    @property
    def create_new_application(self):
        """Returns an application number for work and residence permit.
        """
        new_app = self.request.GET.get('new_application', False)
        if new_app:
            # Generate a new application number
            return '123456'
        return None
