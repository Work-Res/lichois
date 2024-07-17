from django.db import models

from app.models import ApplicationBaseModel


class BaseAssessmentInvestor(ApplicationBaseModel):
    total = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    summary = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Assessment Investor: {self.business_activity}, {self.total}"
