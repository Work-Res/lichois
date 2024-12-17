from django.db import models
from ..choices import EDUCATION_LEVELS
from app.models import ApplicationBaseModel


class Education(ApplicationBaseModel):
    level = models.CharField(
        max_length=50,
        choices=EDUCATION_LEVELS,
        verbose_name="Level/Qualification Equivalence",
        help_text="Select the level or qualification equivalence.",
    )
    field_of_study = models.CharField(
        max_length=100,
        verbose_name="Field or Area of Study",
        help_text="Specify the field or area of study.",
    )
    institution = models.CharField(
        max_length=100,
        verbose_name="Institution",
        help_text="Enter the name of the institution where the qualification was obtained.",
    )
    start_date = models.DateField(
        verbose_name="Start Date",
        help_text="Specify the start date of the program.",
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="End Date",
        help_text="Specify the end date of the program, if applicable.",
    )
    years_attended_full_time = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Years Attended Full-Time",
        help_text="Enter the total number of years spent in formal full-time education, including primary, secondary, and tertiary education.",
    )

    def __str__(self):
        return f"{self.level} in {self.field_of_study} from {self.institution}"

    class Meta:
        app_label = "app"
        verbose_name = "Education Record"
        verbose_name_plural = "Education Records"
        ordering = ["-start_date", "institution"]
