from django.db import models

from base_module.model_mixins import BaseUuidModel

from ..choices import GENDER, YES_NO

from .work_resident_permit import WorkResidencePermit


class Child(BaseUuidModel):

	child_first_name = models.CharField(
		max_length=150)

	child_last_name = models.CharField(
		max_length=150)

	child_age = models.PositiveIntegerField()

	gender = models.CharField(
		max_length=6,
		choices=GENDER)

	is_applying_residence = models.CharField(
		max_length=3,
		choices=YES_NO)

	work_resident_permit = models.ForeignKey(WorkResidencePermit, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Child'
