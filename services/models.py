from django.db import models

# Create your models here.
class TestModel(models.Model):
    name = models.CharField(max_length=100)
    application_number = models.CharField(max_length=100)
    non_citizenship_identifier = models.CharField(max_length=100)

    def __str__(self):
        return self.name