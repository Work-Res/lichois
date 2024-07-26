from django.db import models

from base_module.model_mixins import BaseUuidModel

from .information_request import InformationRequest


class InformationRequestCorrespondence(BaseUuidModel):
    information_request = models.ForeignKey(InformationRequest, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_information_requests_attachments'

    def __str__(self):
        return f"Attachment for {self.information_request.process_name} by {self.information_request.submitter}"

    class Meta:
        db_table = 'app_information_requests_correspondences'
