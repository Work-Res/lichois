# services.py

import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from app.models import Application
from authentication.models import User
from gazette.exceptions import ApplicationNotFoundException, UserNotFoundException, LegalAssessmentNotFoundException, \
    BatchNotFoundException
from gazette.models import LegalAssessment, Batch

logger = logging.getLogger(__name__)


class LegalAssessmentService:
    @staticmethod
    def create_assessment(application_id, legal_member_id, assessment_text):
        try:
            application = Application.objects.get(id=application_id)
            legal_member = User.objects.get(id=legal_member_id)
            assessment = LegalAssessment.objects.create(
                application=application,
                legal_member=legal_member,
                assessment_text=assessment_text
            )
            logger.info(f"Assessment created with ID {assessment.id} by user {legal_member.username} for application "
                        f"{application.application_document.document_number}")
            return assessment
        except ObjectDoesNotExist as e:
            if 'Application' in str(e):
                logger.error(f"Application with ID {application_id} does not exist")
                raise ApplicationNotFoundException()
            elif 'User' in str(e):
                logger.error(f"User with ID {legal_member_id} does not exist")
                raise UserNotFoundException()

    @staticmethod
    def update_assessment(assessment_id, assessment_text):
        try:
            assessment = LegalAssessment.objects.get(id=assessment_id)
            assessment.assessment_text = assessment_text
            assessment.save()
            logger.info(f"Assessment with ID {assessment.id} updated")
            return assessment
        except ObjectDoesNotExist as e:
            logger.error(f"Assessment with ID {assessment_id} does not exist")
            raise LegalAssessmentNotFoundException()

    @staticmethod
    def get_assessment(assessment_id):
        try:
            assessment = LegalAssessment.objects.get(id=assessment_id)
            return assessment
        except ObjectDoesNotExist as e:
            logger.error(f"Assessment with ID {assessment_id} does not exist")
            raise LegalAssessmentNotFoundException()

    @staticmethod
    def complete_batch_assessment(batch_id, legal_member_id):
        try:
            batch = Batch.objects.get(id=batch_id)
            legal_member = User.objects.get(id=legal_member_id)
            assessments = LegalAssessment.objects.filter(batch=batch)

            with transaction.atomic():
                for assessment in assessments:
                    assessment.status = 'COMPLETED'
                    assessment.save()

                batch.status = 'COMPLETED'
                batch.save()

            logger.info(f"Batch assessment with ID {batch_id} declared completed by {legal_member.username}")
            return batch
        except ObjectDoesNotExist as e:
            if 'Batch' in str(e):
                logger.error(f"Batch with ID {batch_id} does not exist")
                raise BatchNotFoundException()
            elif 'User' in str(e):
                logger.error(f"User with ID {legal_member_id} does not exist")
                raise UserNotFoundException()
