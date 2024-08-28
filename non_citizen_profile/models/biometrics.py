from django.db import models

class Biometrics(models.Model):
    non_citizen_id = models.IntegerField(primary_key=True)
    facial_image = models.URLField()
    fingerprint = models.BinaryField()
    biometric_timestamp = models.DateTimeField