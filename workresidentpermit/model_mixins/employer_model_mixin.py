from django.db import models


class EmployerModelMixin(models.Model):
	business_name = models.CharField(max_length=255)
	address = models.TextField()
	tel = models.CharField(max_length=20)
	fax = models.CharField(max_length=20)
	type_of_service = models.CharField(max_length=255)
	job_title = models.CharField(max_length=255)
	job_description = models.TextField()
	renumeration = models.DecimalField(max_digits=10, decimal_places=2)
	period_permit_sought = models.IntegerField()
	has_vacancy_advertised = models.BooleanField()
	have_funished = models.BooleanField()
	reasons_funished = models.TextField()
	time_fully_trained = models.IntegerField()
	reasons_renewal_takeover = models.TextField()
	reasons_recruitment = models.TextField()
	labour_enquires = models.TextField()
	no_bots_citizens = models.IntegerField()
	
	class Meta:
		app_label = 'work_residence_permit'
		abstract = True
