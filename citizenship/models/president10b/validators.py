# app/validators.py

from django.core.exceptions import ValidationError

def validate_citizenship_loss_circumstances(present_citizenship, citizenship_loss_circumstances):
    """
    Validator to ensure that if present_citizenship is null,
    citizenship_loss_circumstances must be provided.
    """
    if present_citizenship is None and citizenship_loss_circumstances is None:
        raise ValidationError("If no present citizenship, circumstances under which it was lost must be provided.")