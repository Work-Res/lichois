from django.db import models


class TraditionalLeader(models.Model):
    kgosi_surname = models.CharField(max_length=255)  # Surname of the Kgosi (traditional leader)
    kgosi_first_name = models.CharField(max_length=255)  # First name of the Kgosi
    kgosana_surname = models.CharField(max_length=255)  # Surname of the Kgosana (sub-leader or assistant)
    kgosana_first_name = models.CharField(max_length=255)  # First name of the Kgosana
    ward_name = models.CharField(max_length=255)  # Name of the ward

    def __str__(self):
        return f"Kgosi: {self.kgosi_surname}, Kgosana: {self.kgosana_surname}, Ward: {self.ward_name}"
