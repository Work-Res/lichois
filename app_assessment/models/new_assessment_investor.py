from django.db import models

from .base_assessment_investor import BaseAssessmentInvestor


class NewAssessmentInvestor(BaseAssessmentInvestor):
    business_activity = models.IntegerField(default=0)
    # business_activity_comment = models.TextField(null=True, blank=False)
    qualification = models.IntegerField(default=0)
    # qualification_comment = models.TextField(null=True, blank=False)
    equity_investment = models.IntegerField(default=0)
    # equity_investment_comment = models.TextField(null=True, blank=False)
    total_investment = models.IntegerField(default=0)
    # total_investment_comment = models.TextField(null=True, blank=False)
    number_of_batswana_employees = models.IntegerField(default=0)
    # number_of_batswana_employees_comment = models.TextField(null=True, blank=False)
    proportion_partners = models.IntegerField(default=0)
    # proportion_partners_comment = models.TextField(null=True, blank=False)
    communication = models.IntegerField(default=0)
    # communication_comment = models.TextField(null=True, blank=False)
    general_experience = models.IntegerField(default=0)
    # general_experience_comment = models.TextField(null=True, blank=False)
    residence = models.IntegerField(default=0)
    # residence_comment = models.TextField(null=True, blank=False)

    class Meta:

        verbose_name = "New Assessment Investors"
        verbose_name_plural = "New Assessment Investors"

    def __str__(self):
        return f"Assessment Investor: {self.business_activity}, {self.total}"
