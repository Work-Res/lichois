from django.db import models

from ..choices import EDUCATION_LEVELS

from app.models import ApplicationBaseModel


class Education(ApplicationBaseModel):

    level = models.CharField(max_length=50, choices=EDUCATION_LEVELS, verbose_name="Level/Qualification Equivalence")
    field_of_study = models.CharField(max_length=100, verbose_name="Fields or area of study")
    institution = models.CharField(max_length=100, verbose_name="Qualifications")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    years_attended_full_time = models.IntegerField(blank=True, null=True, verbose_name="For how many years did you attend formal full time education? Give the total of primary secondary and full time tertiary education if any.")

    def __str__(self):
        return f"{self.level} in {self.field_of_study} from {self.institution}"
