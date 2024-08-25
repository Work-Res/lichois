from django.db import models
from app.models import Application
from authentication.models.user import User


class Objection(models.Model):

    application = models.ForeignKey(
        Application, related_name="objections", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to="objections/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Review fields
    reviewed_by = models.ForeignKey(
        User,
        related_name="reviewed_objections",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_valid = models.BooleanField(
        null=True, blank=True
    )  # True = valid, False = invalid, None = not reviewed
    reviewed_at = models.DateTimeField(null=True, blank=True)

    review_comment = models.TextField(blank=True, null=True)  # Officer's comment

    def __str__(self):
        return f"Objection by {self.name} for {self.application.applicant_name}"
