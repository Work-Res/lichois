from django.db import models
from base_module.model_mixins import BaseUuidModel
from ..models import ProhibitedImmigrant, AuthorizeDetention  

class Detain(BaseUuidModel, models.Model):
    pi = models.ForeignKey(ProhibitedImmigrant, on_delete=models.CASCADE, related_name='detentions')
    authorization = models.ForeignKey(AuthorizeDetention, on_delete=models.SET_NULL, null=True, blank=True, related_name='detained')
    detention_start_date = models.DateTimeField()
    detention_end_date = models.DateTimeField(null=True, blank=True)
    detention_location = models.CharField(max_length=255)
    detained_by = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)  

    def __str__(self):
        end_date = self.detention_end_date or "Ongoing"
        return f"Detention of {self.pi.name} from {self.detention_start_date} to {end_date} at {self.detention_location}"
