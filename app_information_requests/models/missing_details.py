from django.db import models

from app_information_requests.models import InformationRequest


class InformationMissingRequest(models.Model):
    parent_object_id = models.CharField(max_length=255)
    parent_type = models.CharField(max_length=255)
    information_request = models.ForeignKey(InformationRequest, related_name='missing_requests',
                                            on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    description = models.TextField()
    is_provided = models.BooleanField(default=False)

    def __str__(self):
        return f"Missing Request for {self.parent_type} - {self.parent_object_id}"

    class Meta:
        db_table = 'app_information_requests_information_missing_request'
