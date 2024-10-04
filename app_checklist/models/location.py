from django.db import models

from base_module.model_mixins import BaseUuidModel


class LocationTypeEnum(models.TextChoices):

    DISTRICT = 'DISTRICT', 'DISTRICT'
    TOWN = 'TOWN', 'TOWN'
    VILLAGE = 'VILLAGE', 'VILLAGE'
    WARD = 'WARD', 'WARD'


class Location(BaseUuidModel):

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=250)

    parent_location = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_locations'
    )

    location_type = models.CharField(
        max_length=50,  # Adjust the max_length according to the enum values
        choices=LocationTypeEnum.choices,
        null=False
    )

    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'app_checklist_location'

    def __str__(self):
        return f"{self.name} ({self.code})"
