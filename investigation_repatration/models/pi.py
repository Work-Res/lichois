from django.db import models
from identifier.non_citizen_identifier_model_mixins import (
    UniqueNonCitizenIdentifierFieldMixin,
)

# Define choices for the status field
STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Authorized", "Authorized"),
    ("Detained", "Detained"),
    ("Deported", "Deported"),
    ("Released", "Released"),
]


class ProhibitedImmigrant(UniqueNonCitizenIdentifierFieldMixin, models.Model):
    entry_date = models.DateTimeField(null=True, blank=True)
    reason_for_prohibition = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    additional_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.non_citizen_identifier} "
