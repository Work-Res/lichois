from django.db import models

from base_module.model_mixins import BaseUuidModel


class RenunciationAttachment(BaseUuidModel):

    document_number = models.CharField(max_length=100, null=False, blank=False)

    document = models.FileField(upload_to='renunciation_attachments/')

    def __str__(self):
        return f"RenunciationAttachment {self.id}"
