from app.models.application_document import ApplicationDocument
from app.utils import ApplicationStatusEnum
from app.models import ApplicationUser, ApplicationStatus, Application


class ApplicationRepository:
    """
    Repository for managing application and user records.
    """

    @staticmethod
    def get_existing_application(
        application_identifier, status, process_name, application_type
    ):
        """
        Get existing application with a new status for the applicant.
        """
        return Application.objects.filter(
            application_status__code__in=status,
            application_document__applicant__user_identifier=application_identifier,
            process_name=process_name,
            application_type=application_type,
        )

    @staticmethod
    def get_application_status(status, process_name):
        """
        Get existing application status for a particular process.
        """
        return ApplicationStatus.objects.get(
            code__iexact=status or ApplicationStatusEnum.NEW.value,
            processes__icontains=process_name,
        )

    @staticmethod
    def get_or_create_application_user(user_identifier, defaults):
        """
        Create or get an existing application user based on the given user identifier.
        """
        return ApplicationUser.objects.get_or_create(
            user_identifier=user_identifier, defaults=defaults
        )

    @staticmethod
    def get_application_user_by_document_number(document_number):
        """
        Get the application user by document number.
        """
        return ApplicationDocument.objects.get(
            document_number=document_number
        ).applicant

    @staticmethod
    def save_application_document(application_document):
        """
        Save the application document.
        """
        application_document.save()

    @staticmethod
    def save_application(application):
        """
        Save the application.
        """
        application.save()

    @staticmethod
    def save_application_version(application_version):
        """
        Save the application version.
        """
        application_version.save()
