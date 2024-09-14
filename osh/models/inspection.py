from django.db import models

class Inspection(models.Model):
    CATEGORY_CHOICES = [
        ('GENERAL', 'General'),
        ('STEAM_BOILERS', 'Steam Boilers'),
        ('STEAM_RECEIVERS', 'Steam Receivers'),
        ('STEAM_CONTAINERS', 'Steam Containers'),
        ('AIR_RECEIVERS', 'Air Receivers'),
        ('SUPER_HEATERS', 'Super Heaters'),
        ('ECONOMIZERS', 'Economizers'),
        ('CHAINS', 'Chains'),
        ('CRANES', 'Cranes'),
        ('HOISTS', 'Hoists and Lifts'),
    ]

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )
    year = models.IntegerField()
    status = models.CharField(max_length=200)
    registration_date = models.DateField()
    erection_permission_date = models.DateField()
    internal_inspection_date = models.DateField()
    external_inspection_date = models.DateField()
