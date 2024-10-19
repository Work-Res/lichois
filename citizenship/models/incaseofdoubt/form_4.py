from base_module.model_mixins import DeclarationModelMixin, CommissionerOathModelMixin
from django.db import models

from app.models import ApplicationBaseModel
from app_address.models import ApplicationAddress
from app_checklist.models import Location
from app_personal_details.models import Person
from base_module.choices import YES_NO

from citizenship.models.incaseofdoubt.country_visit import CountryVisit


class Form4(ApplicationBaseModel, DeclarationModelMixin, CommissionerOathModelMixin):

    primary_school_attend = models.CharField(max_length=200, null=True, blank=True,
                                             verbose_name="Name of Primary School Attended from standard 1 to 6/7")

    guardian = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_c_child_relations"
    )

    place_of_baptism = models.CharField(max_length=255, blank=True, null=True)

    place_of_baptism = models.CharField(max_length=255, blank=True, null=True)

    date_of_baptism = models.DateField(blank=True, null=True)

    guardian_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_c_guardian_address_of"
    )

    father = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_4_fathers"
    )

    father_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_4_fathers_address_of"
    )

    mother = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_4_mothers"
    )

    mother_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_4_mother_address_of"
    )

    botswana_held_documents = models.BooleanField(default=False)

    particulars_of_botswana_held_documents = models.TextField(blank=True, null=True)

    witness = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_c_witnessing_persons"
    )

    witness_address = models.ForeignKey(
        ApplicationAddress, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_c_witness_address_of"
    )

    is_witness_signed = models.BooleanField(
        verbose_name="Witness Signature"
    )

    witness_date_of_signature = models.DateField(
        null=True, blank=True, verbose_name="Date of witness's Signature"
    )

    countries_visited = models.ManyToManyField(CountryVisit, related_name='countries_visited')

    traditional_leader = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, blank=True,
        related_name="form_4_mothers"
    )


    class Meta:
        app_label = 'citizenship'
        db_table = 'citizenship_form_c'

    def __str__(self):
        return f"Form  - {self.id}"
