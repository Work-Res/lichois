from django.db import models

from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date

from app_personal_details.models import Child


@receiver(pre_save, sender=Child)
def calculate_age_and_status(sender, instance, **kwargs):
    if instance.dob:  # Calculate age only if DOB is provided
        today = date.today()
        instance.age = today.year - instance.dob.year - (
            (today.month, today.day) < (instance.dob.month, instance.dob.day)
        )
        # Update is_minor and is_adult based on the age
        instance.is_minor = instance.age < 18
        instance.is_adult = instance.age > 65
    else:
        # If DOB is not provided, reset age, is_minor, and is_adult
        instance.age = 0
        instance.is_minor = False
        instance.is_adult = False
