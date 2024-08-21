from django.db import models

from base_module.model_mixins import BaseUuidModel
from identifier import UniqueNonCitizenIdentifierFieldMixin


class PIDeclarationOrder(
        UniqueNonCitizenIdentifierFieldMixin, BaseUuidModel):

    order_number = models.CharField(max_length=100, unique=True)

    act_reference = models.TextField()

    date_of_order = models.DateField()

    issuing_authority = models.CharField(max_length=255)

    issuing_authority_names = models.CharField(max_length=255)

    status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Revoked', 'Revoked')])

    def __str__(self):
        return f"Order {self.order_number} - {self.fullnames}"

    class Meta:
        verbose_name = "Prohibited Immigrant Declaration Order"
        verbose_name_plural = "Prohibited Immigrant Declaration Orders"


class PIDeclarationOrderAcknowledgement(
        UniqueNonCitizenIdentifierFieldMixin, BaseUuidModel):

    order = models.ForeignKey(
        PIDeclarationOrder,
        on_delete=models.CASCADE,
        related_name="acknowledgements")

    acknowledged_on = models.DateField(auto_now_add=True)

    remarks = models.TextField(blank=True, null=True)

    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)

    def __str__(self):
        return f"Acknowledgement for Order {self.order.order_number} by {self.acknowledged_by}"

    class Meta:
        verbose_name = "Prohibited Immigrant Declaration Order Acknowledgement"
        verbose_name_plural = "Prohibited Immigrant Declaration Order Acknowledgements"