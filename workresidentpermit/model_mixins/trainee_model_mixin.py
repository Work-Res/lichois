from django.db import models


class TraineeModelMixin(models.Model):
	name = models.CharField(max_length=255)
	educational_qualification = models.CharField(max_length=255)
	job_experience = models.TextField()
	take_over_trainees = models.CharField(max_length=255)
	long_term_trainees = models.CharField(max_length=255)
	date_localization = models.DateField()
	
	class Meta:
		app_label = 'work_residence_permit'
		abstract = True
