from django.db import models


class WorkflowHistory(models.Model):
    document_number = models.CharField(max_length=255)  # String field for document number
    create_rules = models.JSONField()  # JSON field for storing creation rules
    source = models.JSONField()  # JSON field for storing the source
    result = models.BooleanField()  # Boolean field for storing the result
    stage = models.CharField(max_length=100)

    def __str__(self):
        return f"WorkflowHistory(document_number={self.document_number}, result={self.result})"

    class Meta:
        verbose_name = "Workflow History"
        verbose_name_plural = "Workflow Histories"
