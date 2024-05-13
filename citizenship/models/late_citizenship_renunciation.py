from django.db import models
from base_module.model_mixins import BaseUuidModel
from base_module.model_mixins import CommissionerOathModelMixin


class LateCitizenshipRenunciation(CommissionerOathModelMixin, BaseUuidModel):

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
    school_testimonial = models.FileField(upload_to=None, max_length=254)
    place_of_residence_id = models.CharField(max_length=20)
    mother_parent_details_id = models.CharField(max_length=20)
    father_parent_details_id = models.CharField(max_length=20)
    #commissioner_oath

    class Meta:
        app_label = 'citizenship'
