from django.db import models
from lichois.visa.choices import ENTRY_FREQ, VISA_TYPES
from base_module.model_mixins import PersonModelMixin
from base_module.model_mixins import BaseUuidModel


class VisaApplication(BaseUuidModel, PersonModelMixin):

    nationality = models.CharField(max_length=150)

    visa_type = models.CharField(
        verbose_name='Type of visa required',
        choices=VISA_TYPES,
        max_length=50)

    no_of_entries = models.CharField(
        verbose_name='Number of entries',
        choices=ENTRY_FREQ,
        max_length=10)

    # bots_address

    # dom_country_address

    occupation = models.TextField()

    qualifications = models.TextField()

    durations_stay = models.IntegerField(
        verbose_name='Proposed length of stay on whether travelling in transit without break of journey',
        default=""
    )

    travel_reasons = models.TextField(
        verbose_name='Reasons in full for wishing to travel to the Republic of Botswana',
        help_text=('(Satisfactory evidence will be required as to the object of the proposed journey. Employees of '
                   'firms or persons acting on behalf of firms must produce certificates from their employers as to '
                   'the nature and physical address of the business on which they are proceeding abroad. Bankers '
                   'reference may be required.)')
    )

    # Requested Validity Period of Visa
    requested_valid_from = models.DateField(
        verbose_name='From',
        # validators=[date_not_past]
    )

    requested_valid_to = models.DateField(
       verbose_name='To',
       # validators=[date_not_past]
    )

    # References(2) in country of destination(with names, physical address, telephone no, residence permit no, id no)

    # Please indicate what money or cash (amount) will be at your disposal during your visit m2m?

    return_visa_to = models.CharField(
         max_length=100)

    return_valid_until = models.DateField(
        verbose_name='Valid until',
        # validators=[date_not_past]
    )

    # preferred_contact_fields

    class Meta:
        app_label = 'visa'
