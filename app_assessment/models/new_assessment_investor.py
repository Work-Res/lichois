from django.db import models

from .assessment_update_mixin import AssessmentUpdateMixin
from .base_assessment_investor import BaseAssessmentInvestor


class NewAssessmentInvestor(BaseAssessmentInvestor, AssessmentUpdateMixin):
    business_activity = models.IntegerField(default=0)
    qualification = models.IntegerField(default=0)
    equity_investment = models.IntegerField(default=0)
    total_investment = models.IntegerField(default=0)
    number_of_batswana_employees = models.IntegerField(default=0)
    proportion_partners = models.IntegerField(default=0)
    communication = models.IntegerField(default=0)
    general_experience = models.IntegerField(default=0)
    residence = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_assessment()

    class Meta:

        verbose_name = "New Assessment Investors"
        verbose_name_plural = "New Assessment Investors"

    def __str__(self):
        return f"Assessment Investor: {self.business_activity}, {self.total}"
