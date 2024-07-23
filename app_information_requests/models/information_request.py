from django.db import models

from app.models import ApplicationBaseModel
from authentication.models import User


class InformationRequest(ApplicationBaseModel):

    resolution = models.BooleanField(default=False)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    process_name = models.CharField(max_length=255)
    application_type = models.CharField(max_length=255)
    office_location = models.CharField(max_length=255)
    due_date = models.DateField()

    class Meta:
        db_table = 'app_information_requests_information_request'

    def __str__(self):
        return f"Request by {self.submitter} for {self.process_name}"
