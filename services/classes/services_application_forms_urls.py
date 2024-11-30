from django.urls import reverse
from .admin_url_generator import AdminURLGenerator


class ServicesApplicationFormsUrls:
    def __init__(self, application_number=None, application_models_cls=None, next_url=None):
        self.application_number = application_number
        self.application_models_cls = application_models_cls or []
        self.next_url = next_url

    def application_urls(self):
        """Returns a dictionary of application forms, their URLs, and the corresponding object."""
        urls = {}
        next_url_reversed = reverse(self.next_url) if self.next_url else None

        for model_cls in self.application_models_cls:
            urls[model_cls.__name__] = self._get_url_for_model(model_cls, next_url_reversed)

        print(urls, 'urls %%%%%%%%%%%%%^^^^^^^^^^^^^&&&&&&&&&&&&&&')
        return urls

    def _get_url_for_model(self, model_cls, next_url):
        """Helper method to get the URL and object for a specific model."""
        try:
            # Attempt to retrieve the object by document_number
            obj = model_cls.objects.get(document_number=self.application_number)
            # Object exists; generate change URL
            change_url = AdminURLGenerator(model_cls).get_change_url(
                self.application_number, next_url=next_url
            )
            return [change_url, obj]
        except model_cls.DoesNotExist:
            # Object does not exist; generate add URL
            add_url = AdminURLGenerator(model_cls).get_add_url(next_url=next_url)
            return [add_url, None]
