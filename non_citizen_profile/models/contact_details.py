from django.db import models

class ContactDetails(models.Model):
    non_citizen_id = models.IntegerField(primary_key=True)
    # review model:  base_module, simple history
    telphone = models.IntegerField()
    cellphone = models.IntegerField()
    alt_cellphone = models.IntegerField()
    email = models.EmailField()
    alt_email = models.EmailField()
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_number = models.CharField(max_length=15)  