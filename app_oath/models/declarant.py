from django.db import models

from app.models import ApplicationBaseModel


class Declarant(ApplicationBaseModel):

    citizen_of_botswana = models.BooleanField()
    citizen_of_country = models.CharField(max_length=200)
    country_of_birth = models.CharField(max_length=200)
    place_of_birth = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    full_age = models.BooleanField()
    married_person = models.BooleanField(null=True, blank=True)  # Nullable for deleting if not applicable
    not_ordinary_resident = models.BooleanField(null=True, blank=True)  # Nullable for deleting if not applicable
    particulars_true = models.BooleanField()
    renounce_citizenship = models.BooleanField(default=True)
    signature_of_declarant = models.ImageField(upload_to='signatures/', null=True, blank=True)

    class Meta:
        app_label = 'app_oath'
        db_table = 'app_oath_declarant'
