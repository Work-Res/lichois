from django.db import models

from .base_assessment_investor import BaseAssessmentInvestor


class RenewalAssessmentInvestor(BaseAssessmentInvestor):
    capital_investment = models.IntegerField(default=0)
    employment_creation = models.IntegerField(default=0)
    compliance = models.IntegerField(default=0)
    social_investment = models.IntegerField(default=0)

    class Meta:

        verbose_name = "Renewal Assessment Investors"
        verbose_name_plural = "Renewal Assessment Investors"

    def __str__(self):
        return f"Assessment Investor: {self.capital_investment}, {self.total}"
