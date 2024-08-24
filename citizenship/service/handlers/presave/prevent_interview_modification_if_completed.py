from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from citizenship.models import Interview


@receiver(pre_save, sender=Interview)
def prevent_interview_modification_if_completed(sender, instance, **kwargs):
    """
    Signal handler to prevent modification of an Interview if its status is 'completed'.
    """
    if (
        instance.pk
    ):  # This ensures we're dealing with an existing instance, not a new one.
        try:
            existing_interview = Interview.objects.get(pk=instance.pk)
            if (
                existing_interview.status == "completed"
                and instance.status != "completed"
            ):
                raise ValidationError(
                    f"Interview {instance.pk} cannot be modified because it is already completed."
                )
        except Interview.DoesNotExist:
            # If the interview does not exist, we can ignore this
            pass
