from django.db import models
from base_module.model_mixins import BaseUuidModel


class LateCitizenshipRenunciation(BaseUuidModel):

    last_name = models.CharField(max_length=190)
    first_name = models.CharField(max_length=190)
    dob = models.DateField()
    vouch_relatives = models.TextField(max_length=350) #TODO: reevaluate field
    primary_school_attended = models.CharField(max_length=250)
    secondary_school_attended = models.CharField(max_length=250)
    tribal_authority_surname = models.CharField(max_length=250)
    tribal_authority_address = models.TextField(max_length=400)
    ward_name = models.CharField(max_length=190)
    #TODO: school_testimonial_attachment
    #Place of residence model
    #parent_details
    #commissioner_oath

    class Meta:
        app_label = 'citizenship'
