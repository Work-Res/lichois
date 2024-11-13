from django.db import models
from app.models import ApplicationBaseModel

class CompanyAssets(ApplicationBaseModel):

    assert_name = models.CharField(max_length=255, null=True, blank=True)
    assert_value = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    registration_number = models.CharField(max_length=50, blank=True)
    date_acquired = models.DateField()

    def __str__(self):
        return f"{self.assert_name} - {self.registration_number}"

    class Meta:
        verbose_name = "Company Assets"