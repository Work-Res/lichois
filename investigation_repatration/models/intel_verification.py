from django.db import models
from base_module.model_mixins import BaseUuidModel
from non_citizen_profile.models import Biometrics, PersonalDetails, Passport
from identifier.identifier import UniqueNonCitizenIdentifierFieldMixin


class IntelVerification(BaseUuidModel, UniqueNonCitizenIdentifierFieldMixin):
    
    '''
    Model manages the verification of intelligence data.
    '''
    
    fingerprint = models.ForeignKey(Biometrics, on_delete=models.SET_NULL, null=True, blank=True)
    
    permit_no = models.CharField(max_length=50, null=True, blank=True)
    
    non_citizen_id = models.ForeignKey(PersonalDetails, on_delete=models.SET_NULL, null=True, blank=True)
    
    passport = models.ForeignKey(Passport, on_delete=models.SET_NULL, null=True, blank=True)
    
    verification_date = models.DateTimeField(auto_now_add=True)
    
    verified_by = models.CharField(max_length=255)  