import logging
from django.db import transaction
from django.core.exceptions import ValidationError

from app.models import Application
from citizenship.models.board import Meeting, Batch, BatchApplication, Attendee, ConflictOfInterest
from citizenship.models.board.meeting_session import MeetingSession
from citizenship.validators.board.application_eligibility_validator import ApplicationEligibilityValidator

logger = logging.getLogger(__name__)


class BatchService:
    @staticmethod
    @transaction.atomic
    def create_batch(meeting_id, name):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
            batch = Batch.objects.create(
                meeting=meeting,
                name=name
            )
            logger.info(f'Batch created: {batch}')
            return batch
        except Meeting.DoesNotExist:
            logger.error(f'Meeting does not exist: {meeting_id}')
            raise ValidationError("Meeting does not exist.")
        except Exception as e:
            logger.error(f'Error creating batch: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def add_application_to_batch(batch_id, document_number, session_id):
        try:
            if not ApplicationEligibilityValidator().is_eligible(document_number=document_number):
                logger.error(f'Application {document_number} is not eligible to be added to batch {batch_id}')
                raise ValidationError("Application is not eligible to be added to the batch.")

            batch = Batch.objects.get(id=batch_id)
            application = Application.objects.get(document_number=document_number)
            session = MeetingSession.objects.get(id=session_id)
            BatchApplication.objects.create(
                batch=batch,
                application=application,
                session=session
            )
            logger.info(f'Application {application} added to batch {batch}')
            return True
        except Batch.DoesNotExist:
            logger.error(f'Batch does not exist: {batch_id}')
            raise ValidationError("Batch does not exist.")
        except Application.DoesNotExist:
            logger.error(f'Application does not exist: {document_number}')
            raise ValidationError("Application does not exist.")
        except MeetingSession.DoesNotExist:
            logger.error(f'Session does not exist: {session_id}')
            raise ValidationError("Session does not exist.")
        except Exception as e:
            logger.error(f'Error adding application to batch: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def add_applications_to_batch(batch_id, document_numbers, session_id):
        try:
            batch = Batch.objects.get(id=batch_id)
            session = MeetingSession.objects.get(id=session_id)
            applications = Application.objects.filter(document_number__in=document_numbers)

            for application in applications:
                if not ApplicationEligibilityValidator.is_eligible(application):
                    logger.error(f'Application {application.id} is not eligible to be added to batch {batch_id}')
                    raise ValidationError(f"Application {application.id} is not eligible to be added to the batch.")

                BatchApplication.objects.create(
                    batch=batch,
                    application=application,
                    session=session
                )
                logger.info(f'Application {application} added to batch {batch}')
            return True
        except Batch.DoesNotExist:
            logger.error(f'Batch does not exist: {batch_id}')
            raise ValidationError("Batch does not exist.")
        except Application.DoesNotExist:
            logger.error(f'One or more applications do not exist.')
            raise ValidationError("One or more applications do not exist.")
        except MeetingSession.DoesNotExist:
            logger.error(f'Session does not exist: {session_id}')
            raise ValidationError("Session does not exist.")
        except Exception as e:
            logger.error(f'Error adding applications to batch: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def remove_application_from_batch(batch_id, application_id):
        try:
            batch_application = BatchApplication.objects.get(batch_id=batch_id, application_id=application_id)
            batch_application.delete()
            logger.info(f'Application {application_id} removed from batch {batch_id}')
            return True
        except BatchApplication.DoesNotExist:
            logger.error(f'BatchApplication does not exist for batch {batch_id} and application {application_id}')
            raise ValidationError("The application is not part of the batch.")
        except Exception as e:
            logger.error(f'Error removing application from batch: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def remove_application_from_batch(batch_id, application_id):
        try:
            batch_application = BatchApplication.objects.get(batch_id=batch_id, application_id=application_id)
            batch_application.delete()
            logger.info(f'Application {application_id} removed from batch {batch_id}')
            return True
        except BatchApplication.DoesNotExist:
            logger.error(f'BatchApplication does not exist for batch {batch_id} and application {application_id}')
            raise ValidationError("The application is not part of the batch.")
        except Exception as e:
            logger.error(f'Error removing application from batch: {e}')
            raise

    @staticmethod
    def get_applications_in_batch(batch_id):
        return BatchApplication.objects.filter(batch_id=batch_id).select_related('application')

    @staticmethod
    @transaction.atomic
    def declare_conflict_of_interest(attendee_id, application_id, has_conflict=False):
        try:
            attendee = Attendee.objects.get(id=attendee_id)
            application = Application.objects.get(id=application_id)
            conflict, created = ConflictOfInterest.objects.get_or_create(
                attendee=attendee,
                application=application,
                has_conflict=True
            )
            if created:
                logger.info(f'Conflict of interest declared: {conflict}')
            return conflict
        except Attendee.DoesNotExist:
            logger.error(f'Attendee does not exist: {attendee_id}')
            raise ValidationError("Attendee does not exist.")
        except Application.DoesNotExist:
            logger.error(f'Application does not exist: {application_id}')
            raise ValidationError("Application does not exist.")
        except Exception as e:
            logger.error(f'Error declaring conflict of interest: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def declare_no_conflict_for_all(attendee_id, batch_id):
        try:
            attendee = Attendee.objects.get(id=attendee_id)
            batch_applications = BatchApplication.objects.filter(batch_id=batch_id)

            for batch_application in batch_applications:
                ConflictOfInterest.objects.update_or_create(
                    attendee=attendee,
                    application=batch_application.application,
                    defaults={'has_conflict': False}
                )
                logger.info(
                    f'No conflict of interest declared for {batch_application.application.document_number} by {attendee.member.user.username}')
            return True
        except Attendee.DoesNotExist:
            logger.error(f'Attendee does not exist: {attendee_id}')
            raise ValidationError("Attendee does not exist.")
        except BatchApplication.DoesNotExist:
            logger.error(f'Batch does not exist: {batch_id}')
            raise ValidationError("Batch does not exist.")
        except Exception as e:
            logger.error(f'Error declaring no conflict of interest for all applications: {e}')
            raise