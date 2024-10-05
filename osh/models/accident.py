from django.db import models

class Accident(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        ('INTERN', 'Intern'),
        ('ATTACHE', 'Attaché'),
        ('TRAINEE', 'Trainee'),
        ('ENTRY', 'Entry Level'),
        ('JUNIOR', 'Junior'),
        ('MID', 'Mid-Level'),
        ('SENIOR', 'Senior'),
        ('LEAD', 'Lead'),
        ('MANAGER', 'Manager'),
        ('CTO', 'Chief Technology Officer'),
        ('CEO', 'Chief Executive Officer'),
        ('DIRECTOR', 'Director'),
        ('EXECUTIVE', 'Executive'),
    ]

    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    injury_time_occupation = models.CharField(max_length=100)
    experience_level = models.CharField(
        max_length=20, 
        choices=EXPERIENCE_LEVEL_CHOICES, 
        default='JUNIOR'
    )
    fatality_status = models.BooleanField(default = False)
    disabled_for_three_days = models.BooleanField(default=False)
    estimated_injury_cost = models.IntegerField(null=True, blank=True)
    injuries_sustained = models.TextField(null=True, blank=True)
    machines_involved = models.BooleanField(default=False)
    injury_nature = models.TextField()


    def format_time(self):
        return self.time.strftime('%H:%M')

    def __str__(self):
        return f"Accident on {self.date} involving {self.injury_time_occupation}"
