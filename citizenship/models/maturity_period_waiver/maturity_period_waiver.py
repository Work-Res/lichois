from django.db import models

from app.models import ApplicationBaseModel


class MaturityPeriodWaiver(ApplicationBaseModel):
    # TODO: Implement fields

    document_number_for_intention = models.CharField(
        max_length=100
    )

    class Meta:
        app_label = 'citizenship'
        db_table = 'citizenship_maturity_waiver'
