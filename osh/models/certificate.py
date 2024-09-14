from django.db import models

class Certificate(models.Model):
    certificate_no = models.IntegerField()
    issue_date = models.DateField()
    director_signature = models.ImageField()
    factory_registration_certificate_no = models.IntegerField(null=True, blank=True)