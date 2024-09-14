from django.db import models

class Appointee(models.Model):
    signature = models.ImageField()