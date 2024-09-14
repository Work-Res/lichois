from django.db import models

class Equipment(models.Model):
    type = models.CharField(max_length = 200)
    work_nature = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)

    def __str__(self):
        return f"{self.type} - {self.work_nature}"