from django.db import models

class DangerousOccurence(models.Model):

    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    damage_description = models.TextField()
    injured_people_no = models.IntegerField()
    injured_people_names = models.TextField()
    estimate_financial_loss = models.IntegerField()
    place = models.CharField(max_length=200)

    def format_time(self):
        return self.time.strftime('%H:%M')
    
    def __str__(self):
        return f"Dangerous Occurrence on {self.date} at {self.format_time()} - {self.place}"