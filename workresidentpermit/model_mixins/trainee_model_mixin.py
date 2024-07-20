from django.db import models


class TraineeModelMixin(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    educational_qualification = models.CharField(max_length=255, null=True, blank=True)
    job_experience = models.TextField(null=True, blank=True)
    take_over_trainees = models.CharField(max_length=255, null=True, blank=True)
    long_term_trainees = models.CharField(max_length=255, null=True, blank=True)
    date_localization = models.DateField(null=True, blank=True)

    class Meta:
        app_label = "work_residence_permit"
        abstract = True
