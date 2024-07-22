from django.dispatch import receiver
from django.db.models.signals import post_save

from app.models.security_clearance import SecurityClearance


@receiver(post_save, sender=SecurityClearance)
def create_next_activity_by_security_clearance(sender, instance, created, **kwargs):
    pass
