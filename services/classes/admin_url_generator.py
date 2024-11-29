from django.urls import reverse
from django.http import Http404

class AdminURLGenerator:
    def __init__(self, model):
        self.model = model
        self.app_label = model._meta.app_label
        self.model_name = model._meta.model_name

    def get_add_url(self, next_url=None):
        """
        Generate the admin URL for adding a new object.
        Optionally include a 'next' parameter for redirection after saving.
        """
        url = reverse(f'admin:{self.app_label}_{self.model_name}_add')
        if next_url:
            url = f"{url}?next={next_url}"
        return url

    def get_change_url(self, application_number, next_url=None):
        """
        Generate the admin URL for changing an existing object identified by application_number.
        Optionally include a 'next' parameter for redirection after saving.
        """
        try:
            obj = self.model.objects.get(application_number=application_number)
        except self.model.DoesNotExist:
            raise Http404(f"No {self.model_name} found with application_number {application_number}")

        url = reverse(f'admin:{self.app_label}_{self.model_name}_change', args=[obj.pk])
        if next_url:
            url = f"{url}?next={next_url}"
        return url
