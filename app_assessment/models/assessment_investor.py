from django.db import models

from app.models import ApplicationBaseModel


class AssessmentInvestor(ApplicationBaseModel):

    business_activity = models.IntegerField(default=0)
    equity_investment = models.IntegerField(default=0)
    total_investment = models.IntegerField(default=0)
    number_of_batswana_employees = models.IntegerField(default=0)
    proportion_partners = models.IntegerField(default=0)
    investor_or_entrepreneur = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    class Meta:

        db_table = 'assessment_investor'
        verbose_name = 'Assessment Investors'
        verbose_name_plural = 'Assessment Investors'

    def __str__(self):
        return f"Assessment Investor: {self.competency}, {self.qualification}"
