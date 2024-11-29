from django.urls import reverse

from ...classes import AdminURLGenerator


class WorkResApplicationForms:
    
    
    def __init__(
            self, application_number=None,
            application_models_cls=None, next_url=None):

        self.application_number = application_number
        self.application_models_cls = application_models_cls
        self.next_url = next_url
        


    def application_urls(self):
        """Returns a dictionary of application forms, their URLs and obj."""
        urls = {}
        for model_cls in self.application_models_cls:
            # try:
                # Attempt to retrieve the object by document_number
            obj = model_cls.objects.filter(document_number=self.application_number)
            # except model_cls.DoesNotExist:
                # Object does not exist; generate add URL
            if obj:
                print(obj, '$$$$$$$$$$$$$$$$')
                change_url = AdminURLGenerator(model_cls).get_change_url(
                    self.application_number, next_url=reverse(self.next_url)
                )
                urls[model_cls.__name__] = [change_url, obj]
            else:
                add_url = AdminURLGenerator(model_cls).get_add_url(
                next_url=reverse(self.next_url))
                urls[model_cls.__name__] = [add_url, None]
                # Object exists; generate change URL
                
        return urls

            