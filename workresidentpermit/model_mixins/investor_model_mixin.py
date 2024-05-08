from django.db import models
from base_module.choices import YES_NO


class InvestorModelMixin(models.Model):
	company_name = models.CharField(max_length=255)
	address = models.TextField()
	tel = models.CharField(max_length=20)
	location = models.CharField(max_length=255)
	services_offered = models.TextField()
	capacity_employed = models.IntegerField()
	draw_salary = models.BooleanField(choices=YES_NO)
	reason_draw_salary = models.TextField()
	salary_per_annum = models.DecimalField(max_digits=10, decimal_places=2)
	reasons_capacity_employed = models.TextField()
	
	class Meta:
		app_label = 'work_residence_permit'
		abstract = True
