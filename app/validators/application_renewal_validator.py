import logging
from datetime import datetime
from validator import Validator

from app.exceptions.application_renewal_exception import RenewalPeriodNotReached
from app_checklist.models import SystemParameterPermitRenewalPeriod
from app_personal_details.models import Permit

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RenewalPeriodValidator(Validator):
    due_at = "date_after_equal:%Y-%m-%d,%Y-%m-%d"


class ApplicationRenewalValidator:
    """
    Business rules for determining if a renewal process can take place.
    """

    def __init__(self, permit: Permit, application_type):
        self.permit = permit
        self.application_type = application_type
        self.valid_period = RenewalPeriodValidator
        self._system_parameter = None
        self.load_system_parameter()

    def load_system_parameter(self):
        """
        Load the system parameter for the permit renewal period based on the application type.
        Logs the result or any issues encountered.
        """
        try:
            logger.info(
                f"Fetching system parameter for application type: {self.application_type}"
            )
            self._system_parameter = SystemParameterPermitRenewalPeriod.objects.get(
                application_type=self.application_type
            )
            logger.info(
                f"System parameter loaded successfully: {self._system_parameter}"
            )
        except SystemParameterPermitRenewalPeriod.DoesNotExist:
            logger.error(
                f"No system parameter found for application type: {self.application_type}"
            )
            raise ValueError(
                f"System parameter not found for application type: {self.application_type}"
            )
        except Exception as e:
            logger.error(
                f"Error fetching system parameter for application type: {self.application_type}, Error: {str(e)}",
                exc_info=True,
            )
            raise

    def is_renewal_allowed(self):
        """
        Determine if renewal is allowed based on the permit duration and remaining time.
        Logs the validation process and any issues encountered.
        """
        try:
            if not self.permit.date_issued or not self.permit.date_expiry:
                logger.error(
                    f"Permit dates are invalid. Date Issued: {self.permit.date_issued}, Date Expiry: "
                    f"{self.permit.date_expiry}"
                )
                raise ValueError("Invalid permit dates.")

            total_duration = (self.permit.date_expiry - self.permit.date_issued).days
            logger.info(f"Total permit duration: {total_duration} days")

            renewal_threshold = total_duration * self._system_parameter.percent
            remaining_days = (self.permit.date_expiry - datetime.now().date()).days
            logger.info(
                f"Remaining days until permit expiry: {remaining_days} days, Renewal threshold: "
                f"{renewal_threshold} days"
            )

            if remaining_days <= renewal_threshold:
                logger.info(
                    f"Permit renewal is allowed for document_number: {self.permit.document_number}"
                )
                return True
            else:
                logger.info(
                    f"Permit renewal is not allowed for document_number: {self.permit.document_number}. "
                    f"Remaining days exceed threshold."
                )
                raise RenewalPeriodNotReached(
                    f"Permit {self.permit.document_number} cannot be renewed as the remaining days exceed the threshold."
                )
                return False
        except Exception as e:
            logger.error(
                f"Error during permit renewal validation for document_number: {self.permit.document_number}, "
                f"Error: {str(e)}",
                exc_info=True,
            )
            raise
