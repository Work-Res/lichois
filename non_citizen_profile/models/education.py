from django.db import models

from app_personal_details.choices import EDUCATION_LEVELS

from app.models import ApplicationBaseModel


class Education(ApplicationBaseModel):
    non_citizen_id = models.IntegerField(primary_key=True)
    level = models.CharField(max_length=50, choices=EDUCATION_LEVELS)
    field_of_study = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.level} in {self.field_of_study} from {self.institution}"
