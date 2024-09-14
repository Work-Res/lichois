from django.db import models

class Report(models.Model):
    submission_date = models.ImageField()
    casuation_no = models.IntegerField()
    action_taken = models.TextField()
    notification_receipt_date = models.DateField()