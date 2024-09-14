from django.db import models

class Appointment(models.Model):
    date = models.DateField()
    signature = models.ImageField()
    responsibilities = models.TextField()

    def __str__(self):
        return f"Appointment on {self.date}"