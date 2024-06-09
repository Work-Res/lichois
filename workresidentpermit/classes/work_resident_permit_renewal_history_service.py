from datetime import datetime

from app.models import ApplicationUser, ApplicationRenewalHistory

from app_personal_details.models import Permit


class HistoryRecord:

    def __init__(self, created, data, modified=None):
        self.created = created
        self.modified = modified
        self.data = data


class WorkResidentPermitRenewalHistoryService:
    """Responsible for creating Work Resident Permit Permit History Records.
    """

    def __init__(self,
                 document_number: str, application_type: str, application_user: ApplicationUser, process_name: str):
        self.document_number = document_number
        self.application_type = application_type
        self.application_user = application_user
        self.process_name = process_name

    def get_previous_permit(self):
        try:
            permit = Permit.objects.get(
                documber_number=self.document_number
            )
        except Permit.DoesNotExists:
            pass
        else:
            return permit

    def prepare_historical_records(self):
        """
        TODO: To handle for multiple recordss
        :return:
        """
        permit = self.get_previous_permit()
        history_obj_json = permit.__dict__ if permit else {} # ??empty historical record???
        records = HistoryRecord(
            created=datetime.now(),
            data=history_obj_json
        )
        return records.__dict__

    def create_application_renewal_history(self):

        historical = ApplicationRenewalHistory.objects.get_or_create(
            application_type=self.application_type,
            application_user=self.application_user,
            process_name=self.process_name,
            defaults={
                "application_type": self.application_type,
                "application_user": self.application_user,
                "process_name": self.process_name,
                "historical_record": self.prepare_historical_records()
            }
        )
        return historical
