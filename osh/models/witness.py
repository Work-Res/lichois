from django.db import models

class Witness(models.Model):
    signature = models.ImageField()