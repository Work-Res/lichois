from django.db import models

class Appointer(models.Model):
    name = models.CharField(max_length = 255)
    designation = models.CharField(max_length = 255)
    signature = models.ImageField()

    def __str__(self):
        return f"{self.name} - {self.designation}"