from django.urls import reverse
from django.http import Http404

class AdminURLGenerator:
    def __init__(self, model):
        self.model = model
        self.app_label = model._meta.app_label
        self.model_name = model._meta.model_name

    def get_add_url(self, non_citizenship_identifier=None, **query_params):
        """
        Generate the admin URL for adding a new object.
        Optionally include a 'non_citizenship_identifier' and other query parameters.
        """
        url = reverse(f'admin:{self.app_label}_{self.model_name}_add')
        if non_citizenship_identifier:
            query_params['non_citizenship_identifier'] = non_citizenship_identifier
        return self.add_query_params(url, query_params)
    
    def get_change_url(self, application_number=None, non_citizenship_identifier=None, **query_params):
        """
        Generate the admin URL for changing an existing object.
        The object can be identified by application_number or non_citizenship_identifier.
        """
        try:
            if application_number:
                obj = self.model.objects.get(application_number=application_number)
            elif non_citizenship_identifier:
                obj = self.model.objects.get(non_citizenship_identifier=non_citizenship_identifier)
            else:
                raise ValueError("Either application_number or non_citizenship_identifier must be provided.")
        except self.model.DoesNotExist:
            raise Http404(f"No {self.model_name} found with the provided identifier.")
    
        url = reverse(f'admin:{self.app_label}_{self.model_name}_change', args=[obj.pk])
        return self.add_query_params(url, query_params)

    def add_query_params(self, url, params):
        """
        Add query parameters to a URL.
        """
        from urllib.parse import urlencode
        if params:
            query_string = urlencode(params)
            return f"{url}?{query_string}"
        return url

