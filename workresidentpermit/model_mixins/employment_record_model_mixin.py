from django.db import models


class EmploymentRecordModelMixin(models.Model):
	employer = models.CharField(max_length=255)
	occupation = models.CharField(max_length=255)
	duration = models.IntegerField()
	names_of_trainees = models.TextField()
	
	class Meta:
		app_label = 'work_residence_permit'
		abstract = True
