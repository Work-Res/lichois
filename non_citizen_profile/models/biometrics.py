from django.db import models
from base_module.model_mixins import BaseUuidModel
from identifier.identifier import UniqueNonCitizenIdentifierFieldMixin


class Biometrics(BaseUuidModel, UniqueNonCitizenIdentifierFieldMixin):
    
    non_citizen_id = models.IntegerField(primary_key=True)
    
    facial_image = models.URLField()
    
    fingerprint = models.BinaryField()
    
    biometric_timestamp = models.DateTimeField