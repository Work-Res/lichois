from django.db import models

class Bearer(models.Model):
    name = models.CharField(max_length = 200)
    photo = models.ImageField()
    signature = models.ImageField()
    identity_no = models.IntegerField()

    def __str__(self):
        return f"{self.name} (ID: {self.identity_no})"