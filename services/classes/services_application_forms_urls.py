from django.urls import reverse
from urllib.parse import unquote

from .admin_url_generator import AdminURLGenerator


class ServicesApplicationFormsUrls:

    def __init__(self, document_number=None,
                 non_citizen_identifier=None,
                 application_models_cls=None, next_url=None):
        
        self.document_number = document_number
        self.non_citizen_identifier = non_citizen_identifier
        self.application_models_cls = application_models_cls or []
        self.next_url = next_url
    
    def application_urls(self):
        """Returns a dictionary of application forms, their URLs, and the corresponding object."""
        urls = {}
        next_url_reversed = reverse(self.next_url) if self.next_url else None
        for item in self.application_models_cls:
            model_cls = item[0]
            admin_site_name = item[1].name
            urls[model_cls.__name__] = self.get_url_for_model(
                model_cls=model_cls, admin_site_name=admin_site_name, next_url=next_url_reversed)
        return urls

    def get_url_for_model(self, model_cls=None, admin_site_name=None, next_url=None):
        """Helper method to get the URL and object for a specific model."""
        try:
            # Attempt to retrieve the object by document_number
            obj = model_cls.objects.get(document_number=self.document_number)
            # Object exists; generate change URL
            change_url = AdminURLGenerator(
                model_cls, admin_site_name=admin_site_name).get_change_url(
                non_citizen_identifier=self.non_citizen_identifier,
                document_number=self.document_number, next=next_url
            )
            return [unquote(change_url), obj]
        except model_cls.DoesNotExist:
            # Object does not exist; generate add URL
            add_url = AdminURLGenerator(
                model_cls, admin_site_name=admin_site_name).get_add_url(
                non_citizen_identifier=self.non_citizen_identifier,
                document_number=self.document_number, next=next_url)
            return [unquote(add_url), None]
