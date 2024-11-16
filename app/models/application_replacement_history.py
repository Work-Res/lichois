from django.db import models

from django.db.models.fields.json import JSONField

from app_comments.models import Comment
from . import ApplicationUser

from base_module.model_mixins import BaseUuidModel


class ApplicationReplacementHistory(BaseUuidModel):
    application_type = models.CharField(max_length=200)  # E.g WORK_PERMIT_EMERGECY
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    application_user = models.ForeignKey(
        ApplicationUser, on_delete=models.CASCADE
    )  # user_identifier
    process_name = models.CharField(max_length=200)  # WORK_RESIDENT_PERMIT
    historical_record = JSONField()  # permit type , can be of anny type o

    def __str__(self):
        return f"{self.application_type} {self.process_name} {self.application_user.user_identifier}"

    class Meta:
        app_label = "app"
