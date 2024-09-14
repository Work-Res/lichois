from django.db import models

class Referee(models.Model):
    name = models.CharField(max_length=200)
    