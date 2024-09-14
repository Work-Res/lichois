from django.db import models

class Premise(models.Model):
    work_particular = models.CharField(max_length = 200)
    type = models.CharField(max_length = 200)
    work_nature = models.CharField(max_length = 200)
    registration_no = models.IntegerField()
    