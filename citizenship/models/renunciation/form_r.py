from django.db import models

from base_module.model_mixins import BaseUuidModel

from app_address.models import ApplicationAddress
from app_oath.models import Declarant, OathDocument
from app_personal_details.models import Person


class FormR(BaseUuidModel):

    personal_details = models.ForeignKey(Person, on_delete=models.CASCADE)

    address = models.ForeignKey(ApplicationAddress, on_delete=models.CASCADE)

    declarant = models.ForeignKey(Declarant, on_delete=models.CASCADE)

    commissioner_of_oath = models.ForeignKey(OathDocument, on_delete=models.CASCADE)

    class Meta:
        app_label = 'citizenship'
        db_table = 'citizenship_form_r'
