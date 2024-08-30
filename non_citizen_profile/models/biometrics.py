from django.db import models
from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierFieldMixin,
)


class Biometrics(UniqueNonCitizenIdentifierFieldMixin, models.Model):
    facial_image = models.URLField()
    fingerprint = models.BinaryField()
    biometric_timestamp = models.DateTimeField
