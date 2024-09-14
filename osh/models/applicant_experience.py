from django.db import models

class ApplicantExperience(models.Model):
    type = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.type} from {self.start_date} to {self.end_date}"