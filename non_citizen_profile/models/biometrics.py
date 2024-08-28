from django.db import models
from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierModelMixin,
)


class Biometrics(UniqueNonCitizenIdentifierModelMixin, models.Model):
    non_citizen_id = models.IntegerField(primary_key=True)
    facial_image = models.URLField()
    fingerprint = models.BinaryField()
    biometric_timestamp = models.DateTimeField
