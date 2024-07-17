from django.db import models

from base_module.model_fields import UUIDAutoField
from app.models import ApplicationBaseModel

NOTE_TYPE = (
    ('GENERAL', 'GENERAL'),
    ('business', 'REJECT_COMMENT'),
    ('NOTE', 'NOTE')
)


class AssessmentCaseNote(ApplicationBaseModel):

    parent_object_id = UUIDAutoField(
        blank=True,
        editable=False,
        help_text="Parent ID primary key.")

    parent_object_type = models.CharField(
        max_length=200,
        null=False,
        blank=True)

    note_text = models.TextField()

    note_type = models.CharField(
        max_length=200,
        choices=NOTE_TYPE,
        null=False,
        blank=True)

    class Meta:
        db_table = 'assessment_case_note'
        verbose_name = 'Assessment Case Note'
        verbose_name_plural = 'Assessment Case Note'
