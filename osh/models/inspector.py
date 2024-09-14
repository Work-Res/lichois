from django.db import models

class Inspector(models.Model):
    name = models.CharField(max_length = 255)
    sworn_date = models.DateField()
    inspector_category = models.CharField(max_length=200)