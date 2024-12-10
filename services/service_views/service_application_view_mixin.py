from ..classes import ServicesApplicationFormsUrls


class ServiceApplicationViewMixin:
    
    def application_forms(self, model_cls_list=None, next_url=None):
        """Returns application forms and urls.
        """
    
        forms_urls = ServicesApplicationFormsUrls(
            document_number=self.application_number(),
            non_citizen_identifier=self.non_citizen_identifier,
            application_models_cls=model_cls_list,
            next_url=next_url).application_urls()
        return forms_urls

    def application_number(self):
        """Returns an application number.
        """
        application_number = '12345' #self.request.GET.get('application_number', '')
        
        #Impliment this method to get a permit application number for a permit being applied for.
        
        return application_number

    @property
    def non_citizen_identifier(self):
        """Returns the applicant's non_citizen_identifier.
        """
        return self.request.user.non_citizen_identifier

    @property
    def personal_details(self):
        """Returns personal details.
        """
        
        personal_details = {
            'Fullname': f'{self.request.user.first_name} {self.request.user.last_name}',
            'Email': self.request.user.email,
            'Date of Birth': self.request.user.dob,
            'Non Citizen Identifier': self.request.user.non_citizen_identifier}
        return personal_details
    