from django.db import models
from base_module.choices import YES_NO


class PersonalDetailsModelMixin(models.Model):

    last_name = models.CharField(max_length=190)
    first_name = models.CharField(max_length=190)
    middle_name = models.CharField(max_length=190,blank=True,null=True)
    maiden_name = models.CharField(max_length=190,blank=True,null=True)
    dob = models.DateField(blank=True,null=True)
    birth_place = models.CharField(max_length=190,blank=True,null=True)
    birth_country = models.CharField(max_length=190, blank=True, null=True)
    qualification = models.CharField(max_length=500, blank=True, null=True)
    occupation = models.CharField(max_length=500, blank=True, null=True)
    #TODO: check field options
    spouse_citizenship_acquired = models.CharField(max_length=190, blank=True, null=True)
    marriage_subsisting = models.CharField(choices=YES_NO, max_length=5, blank=True, null=True)


    class Meta:
        abstract = True
