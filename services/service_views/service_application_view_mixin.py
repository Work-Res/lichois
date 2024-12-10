from ..classes import ServicesApplicationFormsUrls

from app_personal_details.models import Person


class ServiceApplicationViewMixin:
    

    def application_forms(self, model_cls_list=None, next_url=None):
        """Returns application forms and urls.
        """
    
        forms_urls = ServicesApplicationFormsUrls(
            application_number=self.application_number(),
            non_citizen_identifier=self.non_citizen_identifier(),
            application_models_cls=model_cls_list,
            next_url=next_url).application_urls()
        return forms_urls

    def application_number(self):
        """Returns an application number.
        """
        application_number = '12345' #self.request.GET.get('application_number', '')
        
        #Impliment this method to get a permit application number for a permit being applied for.
        
        return application_number

    def non_citizen_identifier(self):
        """Returns the applicant's non_citizen_identifier.
        """
        return 'NC123412'

    def personal_details(self):
        """Returns personal details.
        """
        
        personal_details = {
            'first_name': self.request.user.firstname,
            'last_name': self.request.user.lastname,
            'email': self.request.user.email,
            'dob': self.request.user.dod}

    def person(self):
        """Returns the person obj.
        """
        try:
            person = Person.objects.get()
        except Person.DoesNotExist:
            return None
        else:
            return person