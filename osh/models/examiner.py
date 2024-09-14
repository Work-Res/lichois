from django.db import models

class Examiner(models.Model):
    name = models.CharField(max_length=200)
    signature = models.ImageField()