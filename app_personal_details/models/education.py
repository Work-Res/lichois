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
    qualification = models.TextField(
        verbose_name="Qualification",
        help_text="Enter the name(s) of your Qualifications.",
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
    relevant_experience = models.TextField(
        blank=True,
        null=True,
        verbose_name="Relevant Work Experience",
        help_text="Enter work experience eg \
            (Hotel X(5years), Primary School(2years))",
    )

    def __str__(self):
        return f"{self.level} in {self.field_of_study} from {self.institution}"

    class Meta:
        app_label = "app_personal_details"
        verbose_name = "Education Record"
        verbose_name_plural=  "Education Records"
        ordering = ["-start_date", "institution"]
