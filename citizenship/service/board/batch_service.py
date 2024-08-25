import logging
from django.db import transaction
from django.core.exceptions import ValidationError

from app.models import Application
from citizenship.models import Meeting, Batch, BatchApplication, Attendee, ConflictOfInterest, Interview
from citizenship.models.board.meeting_session import MeetingSession
from citizenship.validators.board.application_eligibility_validator import ApplicationEligibilityValidator

from .batch_status_enum import BatchStatus
from .interview_service import InterviewService
from ...exception import BatchSizeMaxLimitReachedException

logger = logging.getLogger(__name__)

MAX_APPLICATIONS_PER_SESSION = 200


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
            if not ApplicationEligibilityValidator(document_number=document_number).is_valid():
                logger.error(f'Application {document_number} is not eligible to be added to batch {batch_id}')
                raise ValidationError("Application is not eligible to be added to the batch.")

            batch = Batch.objects.get(id=batch_id)
            session = MeetingSession.objects.get(id=session_id)
            current_application_count = BatchApplication.objects.filter(meeting_session=session).count()

            if current_application_count >= MAX_APPLICATIONS_PER_SESSION:
                session.batch_application_complete = True
                session.save()
                logger.error(f'Session {session_id} has reached its application limit')
                raise BatchSizeMaxLimitReachedException(
                    f'Session {session_id} has reached its application limit of {MAX_APPLICATIONS_PER_SESSION} applications.')

            application = Application.objects.get(application_document__document_number=document_number)
            BatchApplication.objects.create(
                batch=batch,
                application=application,
                meeting_session=session
            )

            # Update the flag if the limit is reached after adding this application
            if current_application_count + 1 >= MAX_APPLICATIONS_PER_SESSION:
                session.batch_application_complete = True
                session.save()
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
            batch = BatchService.get_batch(batch_id)
            session = BatchService.get_meeting_session(session_id)
            applications = BatchService.get_applications_by_document_numbers(document_numbers)
            BatchService.validate_and_add_applications(batch, session, applications)
            return True
        except (Batch.DoesNotExist, Application.DoesNotExist, MeetingSession.DoesNotExist) as e:
            logger.error(e)
            raise ValidationError(str(e))
        except Exception as e:
            logger.error(f'Error adding applications to batch: {e}')
            raise

    @staticmethod
    def get_batch(batch_id):
        try:
            return Batch.objects.get(id=batch_id)
        except Batch.DoesNotExist:
            error_message = f'Batch does not exist: {batch_id}'
            logger.error(error_message)
            raise ValidationError(error_message)

    @staticmethod
    def get_meeting_session(session_id):
        try:
            return MeetingSession.objects.get(id=session_id)
        except MeetingSession.DoesNotExist:
            error_message = f'Session does not exist: {session_id}'
            logger.error(error_message)
            raise ValidationError(error_message)

    @staticmethod
    def get_applications_by_document_numbers(document_numbers):
        applications = Application.objects.filter(application_document__document_number__in=document_numbers)
        if not applications.exists():
            error_message = 'One or more applications do not exist.'
            logger.error(error_message)
            raise ValidationError(error_message)
        logger.info(f"Found list of applications: {applications}")
        return applications

    @staticmethod
    def validate_and_add_applications(batch, session, applications):
        for application in applications:
            document_number = application.application_document.document_number
            BatchService.validate_application_eligibility(application)
            BatchService.create_batch_application(batch, session, application)
            BatchService.set_application_batched(document_number, True)

    @staticmethod
    def validate_application_eligibility(application):
        document_number = application.application_document.document_number
        if not ApplicationEligibilityValidator(document_number=document_number).is_valid():
            error_message = f'Application {application.id} is not eligible to be added to the batch.'
            logger.error(error_message)
            raise ValidationError(error_message)

    @staticmethod
    def create_batch_application(batch, session, application):
        try:
            BatchApplication.objects.create(
                batch=batch,
                application=application,
                meeting_session=session
            )
            logger.info(f'Application {application} added to batch {batch}')
        except ValidationError as e:
            logger.warning(f"{e}")
            raise

    @staticmethod
    def set_application_batched(document_number, batched):
        try:
            application = Application.objects.get(application_document__document_number=document_number)
            application.batched = batched
            application.save()
            logger.info(f"Application {document_number} batched successfully.")
        except Application.DoesNotExist:
            logger.error(f"Application {document_number} not found.")

    @staticmethod
    @transaction.atomic
    def remove_application_from_batch(batch_id, application_id):
        try:
            batch_application = BatchApplication.objects.get(batch_id=batch_id, application_id=application_id)
            batch_application.delete()
            logger.info(f'Application {application_id} removed from batch {batch_id}')
            BatchService.set_application_batched(batch_application.application.application_document.document_number,
                                                 False)
        except BatchApplication.DoesNotExist:
            logger.error(f'BatchApplication does not exist for batch {batch_id} and application {application_id}')
            raise ValidationError("The application is not part of the batch.")
        except Exception as e:
            logger.error(f'Error removing application from batch: {e}')
            raise
        return False


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
    def declare_conflict_of_interest(attendee_id, document_number, has_conflict=False, meeting_session=None,
                                     client_relationship=None, interest_description=None):
        try:
            attendee = Attendee.objects.get(member__user=attendee_id) #Fixme refactor attendee_id to user
            application = Application.objects.get(
                application_document__document_number=document_number)
            created = ConflictOfInterest.objects.create_conflict(
                attendee=attendee,
                application=application,
                has_conflict=has_conflict,
                meeting_session=meeting_session,
                client_relationship=client_relationship,
                interest_description=interest_description
            )
            if created:
                interview_service = InterviewService(
                    application=application, meeting_session=meeting_session)
                interview_service.add_board_member(board_member=attendee.member)
                logger.info(f'Conflict of interest declared: {created}')
            return created
        except Attendee.DoesNotExist:
            logger.error(f'Attendee does not exist: {attendee_id}')
            raise ValidationError("Attendee does not exist.")
        except Application.DoesNotExist:
            logger.error(f'Application does not exist: {document_number}')
            raise ValidationError("Application does not exist.")
        except Exception as e:
            logger.error(f'Error declaring conflict of interest: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def change_batch_status(batch_id, new_status):
        try:
            batch = Batch.objects.get(id=batch_id)
            if new_status == BatchStatus.CLOSED.name:
                if batch.status == BatchStatus.CLOSED.name:
                    raise ValidationError("Batch is already closed.")
                new_applications = BatchApplication.objects.filter(
                    batch=batch).order_by('created')
                logger.info(f"Applications found: {new_applications} to be interviewed. ")
                for batch_application in new_applications:
                    Interview.objects.get_or_create(
                        application=batch_application.application,
                        defaults={
                            'application': batch_application.application,
                            'meeting_session': batch_application.meeting_session,
                            'scheduled_time': batch_application.meeting_session.date,
                            'variation_type': batch_application.application.application_document.applicant_type
                        }
                    )
                logger.info(f'Batch {batch_id} closed and interviews created for new applications.')
            batch.status = new_status
            batch.save()
            return batch
        except Batch.DoesNotExist:
            logger.error(f'Batch does not exist: {batch_id}')
            raise ValidationError("Batch does not exist.")
        except Exception as e:
            logger.error(f'Error changing batch status: {e}')
            raise

    @staticmethod
    @transaction.atomic
    def declare_no_conflict_for_all(attendee_id, batch_id,  meeting_session=None):
        try:
            attendee = Attendee.objects.get(member__user=attendee_id)
            meeting_session = MeetingSession.objects.get(id=meeting_session)
            batch_applications = BatchApplication.objects.filter(
                batch_id=batch_id, meeting_session=meeting_session)
            logger.info(f"Batch applications found: {batch_applications}")
            if not batch_applications.exists():
                raise ValidationError(f"Batch Applications is empty for {batch_id}")
            for batch_application in batch_applications:
                ConflictOfInterest.objects.create_conflict(
                    attendee=attendee,
                    application=batch_application.application,
                    has_conflict=False,
                    meeting_session=meeting_session
                )
                interview_service = InterviewService(
                    application=batch_application.application, meeting_session=meeting_session)
                interview_service.add_board_member(board_member=attendee.member)
                logger.info(
                    f'No conflict of interest declared for {batch_application.application.document_number} by '
                    f'{attendee.member.user.username}')
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
