from django.db import models


class PersonalDetailsModelMixin(models.Model):

    last_name = models.CharField(max_length=190)
    first_name = models.CharField(max_length=190)
    middle_name = models.CharField(max_length=190,blank=True,null=True)
    maiden_name = models.CharField(max_length=190,blank=True,null=True)
    dob = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=190,blank=True,null=True)
    birth_country = models.CharField(max_length=190, blank=True, null=True)
    qualification = models.TextField(max_length=500, blank=True, null=True)
    occupation = models.TextField(max_length=500, blank=True, null=True)
    #TODO: check field options
    #postal_address
    #residential_address


    class Meta:
        abstract = True
