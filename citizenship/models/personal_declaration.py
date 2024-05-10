from django.db import models
from base_module.model_mixins import BaseUuidModel


class PersonalDeclaration(BaseUuidModel):

    settlement_location = models.CharField(max_length=190)
    settlement_village = models.CharField(max_length=190)
    settlement_year = models.DateField()
    citizenship_country = models.TextField(max_length=350)
    community = models.CharField(max_length=150)
    community_member_type = models.CharField(max_length=150)
    kgosi_firstname = models.CharField(max_length=150)
    kgosi_lastname = models.TextField(max_length=150)

    class Meta:
        app_label = 'citizenship'
