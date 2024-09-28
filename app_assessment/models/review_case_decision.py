from django.db import models

from app.models import ApplicationBaseModel, ApplicationDecisionType


class ReviewCaseDecision(ApplicationBaseModel):

    status = models.ForeignKey(
        ApplicationDecisionType, on_delete=models.SET_NULL, null=True
    )

    date_approved = models.DateTimeField(null=True, blank=True)

    approved_by = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.status}"

    class Meta:
        app_label = "app_assessment"
