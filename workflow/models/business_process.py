from django.db import models


from base_module.model_mixins import BaseUuidModel


class BusinessProcess(BaseUuidModel):
    """
    Represents the overall business process e.g VISA, WORK_RESIDENT_PERMIT e.t.c
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    document_number = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Business Process"
        ordering = ['-created']
