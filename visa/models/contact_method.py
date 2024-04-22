from django.db import models
# from base_module.model_mixins import ContactInfoModelMixin
from base_module.model_mixins import BaseUuidModel
from .visa_application import VisaApplication


class ContactMethod(BaseUuidModel):

    visa_application = models.ForeignKey(
        VisaApplication,
        on_delete=models.CASCADE
    )

    class Meta:
        app_label = 'visa'
        unique_together = ('visa_application', 'contact_method',
                           'contact_value')
