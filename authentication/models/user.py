from django.contrib.auth.models import AbstractUser
from django.db import models
from identifier.non_citizen_identifier_model_mixins import (
    NonUniqueNonCitizenIdentifierFieldMixin,
    NonCitizenIdentifierMethodsModelMixin
)


class User(NonUniqueNonCitizenIdentifierFieldMixin, AbstractUser, NonCitizenIdentifierMethodsModelMixin):
    phone_number = models.IntegerField(unique=True, null=True)
    dob = models.DateField(null=True, blank=True)

    def is_chairperson(self):
        return self.groups.filter(name="chairperson").exists()

    def is_board_member(self):
        return self.groups.filter(name="board_member").exists()

    def is_secretary(self):
        return self.groups.filter(name="secretary").exists()

    def is_customer(self):
        return self.groups.filter(name="customer").exists()

    def __str__(self) -> str:
        return self.username
