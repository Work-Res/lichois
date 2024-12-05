from django.db import models


class EmploymentRecordModelMixin(models.Model):
    employer = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    names_of_trainees = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "workresidentpermit"
        abstract = True
