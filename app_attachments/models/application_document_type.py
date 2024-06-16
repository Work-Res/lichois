from django.db import models

from base_module.model_mixins import BaseUuidModel


class AttachmentDocumentType(BaseUuidModel):
    id = models.IntegerField()
    
    code = models.CharField(max_length=100)

    name = models.CharField(max_length=200)

    valid_from = models.DateField()

    valid_to = models.DateField()

    class Meta:
        verbose_name_plural = "Application Document Types"
        ordering = ['-created']
