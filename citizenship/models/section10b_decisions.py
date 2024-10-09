
from base_module.model_mixins import BaseUuidModel
from django.db import models
from app.models import Application
from app.utils import ApplicationDecisionEnum


class Section10bApplicationDecisions(BaseUuidModel):

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        primary_key=False
    )

    mlha_director_decision = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    deputy_permanent_secretary = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    permanent_secretary = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    pres_permanent_secretary = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    president_decision = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        default=ApplicationDecisionEnum.PENDING.value,
    )

    class Meta:
        verbose_name = "Section 10B Application Decision"
        verbose_name_plural = "Section 10B Application Decisions"

    def __str__(self):
        return self._meta.verbose_name
