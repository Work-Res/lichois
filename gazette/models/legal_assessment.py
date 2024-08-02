from django.db import models

from base_module.model_mixins import BaseUuidModel

from app.models import Application
from authentication.models import User
from gazette.models.choices import LEGAL_STATUS_CHOICES


class LegalAssessment(BaseUuidModel):

    status = models.CharField(max_length=20, choices=LEGAL_STATUS_CHOICES, default='IN_PROGRESS')
    application = models.ForeignKey(Application, related_name='assessments', on_delete=models.CASCADE)
    legal_member = models.ForeignKey(User, related_name='assessments', on_delete=models.CASCADE)
    assessment_text = models.TextField()

    def __str__(self):
        return f"Assessment by {self.legal_member.username} for {self.application.title}"
