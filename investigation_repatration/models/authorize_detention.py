from django.db import models
from base_module.model_mixins import BaseUuidModel
from non_citizen_profile.models import Person  

class AuthorizeDetention(BaseUuidModel, models.Model):
    authorized_by = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    detention_reason = models.TextField()
    detention_date = models.DateTimeField(auto_now_add=True)
    detention_location = models.CharField(max_length=255)
    release_conditions = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Detention Authorization for {self.pi.name} by {self.authorized_by.name} on {self.detention_date}"
