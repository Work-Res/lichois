from django.db import models

from app_personal_details.choices import EDUCATION_LEVELS
from base_module.model_mixins import BaseUuidModel
from identifier.identifier import  NonUniqueNonCitizenIdentifierFieldMixin


class Education(BaseUuidModel,NonUniqueNonCitizenIdentifierFieldMixin):
    
    non_citizen_id = models.IntegerField(primary_key=True)
    
    level = models.CharField(max_length=50, choices=EDUCATION_LEVELS)
    
    field_of_study = models.CharField(max_length=100)
    
    institution = models.CharField(max_length=100)
    
    start_date = models.DateField()
    
    end_date = models.DateField(blank=True, null=True)
