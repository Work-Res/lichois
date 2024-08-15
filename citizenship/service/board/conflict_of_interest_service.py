import logging
from django.core.exceptions import ValidationError
from citizenship.models import ConflictOfInterest

logger = logging.getLogger(__name__)


class ConflictOfInterestService:

    @staticmethod
    def get_conflict_of_interest_by_id(id):
        if id:
            return ConflictOfInterest.objects.get(id=id)

    @staticmethod
    def get_conflict_of_interest_by_attendee_and_application(attendee_id, application_id):
        if attendee_id and application_id:
            return ConflictOfInterest.objects.get(attendee__id=attendee_id, application__id=application_id)

    @staticmethod
    def authorize_member_for_interview(pk, attendee_id=None, application_id=None):
        """
        Authorizes a board member with a declared conflict of interest to participate in the interview.

        Args:
            attendee_id (int): The ID of the attendee record.
            application_id (int): The ID of the application record.

        Returns:
            ConflictOfInterest: The updated ConflictOfInterest object.

        Raises:
            ValidationError: If the ConflictOfInterest record does not exist, if the member does not have a declared
            conflict of interest, or if the member has already been authorized.
        """
        try:
            # Fetch the ConflictOfInterest record
            conflict_of_interest = ConflictOfInterestService.get_conflict_of_interest_by_id(pk)
            if not conflict_of_interest:
                ConflictOfInterestService.get_conflict_of_interest_by_attendee_and_application(
                    attendee_id, application_id)
            if conflict_of_interest:
                logger.error("Conflict of interest not found.")
                raise ValidationError("Conflict of interest not found.")
            # Check if the member has already been authorized
            if conflict_of_interest.is_authorized:
                logger.warning(
                    f"Authorization attempt failed: Member {conflict_of_interest.attendee.member.user.username} "
                    f"has already been authorized for application {conflict_of_interest.application.document_number}."
                )
                raise ValidationError("This member has already been authorized to participate in the interview.")

            # Ensure the member has declared a conflict of interest
            if not conflict_of_interest.has_conflict:
                logger.warning(
                    f"Authorization attempt failed: Member {conflict_of_interest.attendee.member.user.username} "
                    f"does not have a declared conflict of interest."
                )
                raise ValidationError("This member does not have a declared conflict of interest.")

            # Authorize the member to participate
            conflict_of_interest.is_authorized = True
            conflict_of_interest.save()

            logger.info(
                f"Member {conflict_of_interest.attendee.member.user.username} "
                f"authorized to participate in the interview for application "
                f"{conflict_of_interest.application.document_number}."
            )

            return conflict_of_interest

        except ConflictOfInterest.DoesNotExist:
            logger.error(
                f"ConflictOfInterest record does not exist for attendee ID {attendee_id} and application ID {application_id}."
            )
            raise ValidationError(
                "Conflict of Interest record does not exist for the provided attendee and application.")

        except ValidationError as e:
            logger.error(f"Validation error during member authorization for interview: {str(e)}")
            raise e

        except Exception as e:
            logger.exception(f"An unexpected error occurred during authorization: {str(e)}")
            raise ValidationError("An unexpected error occurred during authorization.")
