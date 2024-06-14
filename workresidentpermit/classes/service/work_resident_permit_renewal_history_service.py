import json

from datetime import datetime

from app.models import ApplicationUser, ApplicationRenewalHistory

from app_personal_details.models import Permit

from .historical_record import PermitData, historical_record_to_dict, permit_data_to_dict, HistoricalRecord


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

    def prepare_historical_records_to_json(self):
        """
        TODO: To handle for multiple records
        :return:
        """
        permit = self.get_previous_permit()
        # current permit..
        permit_obj = permit.to_dataclass()
        # get the existings

        application_renewal_history = ApplicationRenewalHistory.objects.get(
            application_type=self.application_type,
            application_user=self.application_user,
            process_name=self.process_name
        )
        existing_historical_data = self.json_to_historical_record(
            json_str=application_renewal_history.historical_record)
        existing_historical_data.data.append(permit_obj)

        return existing_historical_data

    def dict_to_permit_data(self, permit_dict: dict) -> PermitData:
        return PermitData(
            permit_type=permit_dict['permit_type'],
            permit_no=permit_dict['permit_no'],
            date_issued=datetime.fromisoformat(permit_dict['date_issued']).date(),
            date_expiry=datetime.fromisoformat(permit_dict['date_expiry']).date(),
            place_issue=permit_dict['place_issue']
        )

    def json_to_historical_record(self, json_str: str) -> HistoricalRecord:
        record_dict = json.loads(json_str)
        permits = [self.dict_to_permit_data(permit) for permit in record_dict['data']]
        return HistoricalRecord(
            created=record_dict['created'],
            data=permits
        )

    def create_application_renewal_history(self):

        historical = ApplicationRenewalHistory.objects.update_or_create(
            application_type=self.application_type,
            application_user=self.application_user,
            process_name=self.process_name,
            defaults={
                "application_type": self.application_type,
                "application_user": self.application_user,
                "process_name": self.process_name,
                "historical_record": historical_record_to_dict(self.prepare_historical_records())
            }
        )
        return historical
