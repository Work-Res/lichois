from django.db import models
from base_module.choices import YES_NO

class TraineeModelMixin(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Name of Trainee")
    educational_qualification = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name="Educational Qualification")
    job_experience = models.TextField(null=True, blank=True, verbose_name="Job Experience")
    take_over_trainees = models.CharField(max_length=255, null=True, blank=True,
                                          verbose_name="Name of trainee most likely to take over at the expiry'\
                                              ' of the permit or in the long run")
    trainee_time = models.PositiveIntegerField(verbose_name="State time required to have trainee fully trained",
                                               help_text="State time in months")
    long_term_trainees = models.CharField(max_length=255, null=True, blank=True)
    date_localization = models.DateField(null=True, blank=True, verbose_name="Date of Localization of the post")

    class Meta:
        app_label = "workresidentpermit"
        abstract = True
