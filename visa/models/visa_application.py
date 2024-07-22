from django.db import models
from ..choices import ENTRY_FREQ, VISA_TYPES

# from base_module.model_mixins import PersonModelMixin
from base_module.model_mixins import BaseUuidModel


class VisaApplication(BaseUuidModel):
    visa_type = models.CharField(choices=VISA_TYPES, max_length=50)
    no_of_entries = models.CharField(choices=ENTRY_FREQ, max_length=10)

    durations_stay = models.IntegerField()

    travel_reasons = models.TextField(
        verbose_name="Reasons in full for wishing to travel to the Republic of Botswana",
        help_text=(
            "(Satisfactory evidence will be required as to the object of the proposed journey. Employees of "
            "firms or persons acting on behalf of firms must produce certificates from their employers as to "
            "the nature and physical address of the business on which they are proceeding abroad. Bankers "
            "reference may be required.)"
        ),
    )

    # Requested Validity Period of Visa
    requested_valid_from = models.DateField()  # validators=[date_not_past]

    requested_valid_to = models.DateField()  # validators=[date_not_past]

    # TODO: References(2) in country of destination(with names, physical address, telephone no,
    # residence permit no, id no)

    # Please indicate what money or cash (amount) will be at your disposal
    # during your visit m2m?

    return_visa_to = models.CharField(max_length=100)

    return_valid_until = models.DateField()  # validators=[date_not_past]

    class Meta:
        app_label = "visa"
