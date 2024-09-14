from django.db import models
from .examination import Examination


class Boiler(models.Model):
    choices = [
        ('NEW','New'),
        ('OLD', 'Old')
    ]

    type = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    manufacture_year = models.IntegerField()
    manufacture_name = models.CharField(max_length = 255)
    manufacture_no = models.IntegerField()
    erection_place = models.CharField(max_length = 255)
    erection_date = models.DateField()
    construction_code = models.CharField(max_length = 10)
    work_no = models.IntegerField()
    max_working_pressure = models.IntegerField(max_length = 10)
    working_pressure = models.IntegerField()
    test_pressure = models.CharField(max_length = 10)
    grate_area = models.CharField(max_length = 50)
    heating_surface = models.CharField(max_length = 255)
    evapouration_capacity = models.IntegerField()
    used_or_new = models.CharField(
        choices=choices, 
        max_length=10, 
        default='NEW'
    )
    previous_location = models.CharField(max_length = 255)
    last_exam_date = models.ForeignKey(Examination, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.type} ({self.manufacture_year}) - {self.used_or_new}"
