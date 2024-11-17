import json

from datetime import date, datetime

from app.models import ApplicationUser, ApplicationRenewalHistory

from app_personal_details.models import Permit

from workresidentpermit.classes.historical_record import (
    PermitData,
    historical_record_to_dict,
    HistoricalRecord,
)


class WorkResidentPermitRenewalHistoryService:
    """Responsible for creating Work Resident Permit Permit History Records."""

    def __init__(
        self,
        document_number: str,
        application_type: str,
        application_user: ApplicationUser,
        process_name: str,
    ):
        self.document_number = document_number
        self.application_type = application_type
        self.application_user = application_user
        self.process_name = process_name

    def get_previous_permit(self):
        try:
            permit = Permit.objects.get(document_number=self.document_number)
        except Permit.DoesNotExist:
            pass
        else:
            return permit

    def prepare_historical_records_to_json(self):
        """
        :return:
        """
        permit = self.get_previous_permit()
        # current permit..
        newly_permit_json = permit.to_dataclass()

        # get existing historical
        application_renewal_history = None
        try:
            application_renewal_history = ApplicationRenewalHistory.objects.get(
                application_type=self.application_type,
                application_user=self.application_user,
                process_name=self.process_name,
            )
        except ApplicationRenewalHistory.DoesNotExist:
            pass

        # Read existing JSON data.
        json_str = (
            application_renewal_history.historical_record
            if application_renewal_history
            else None
        )

        existing_historical_data = self.json_to_historical_record(json_str=json_str)
        if existing_historical_data:
            existing_historical_data.data.append(newly_permit_json)
        return existing_historical_data

    def dict_to_permit_data(self, permit_dict: dict) -> PermitData:
        return PermitData(
            permit_type=permit_dict["permit_type"],
            permit_no=permit_dict["permit_no"],
            date_issued=datetime.fromisoformat(permit_dict["date_issued"]).date(),
            date_expiry=datetime.fromisoformat(permit_dict["date_expiry"]).date(),
            place_issue=permit_dict["place_issue"],
            document_number=permit_dict["document_number"],
        )

    def json_to_historical_record(self, json_str: str) -> HistoricalRecord:
        if json_str:
            if isinstance(json_str, str):
                record_dict = json.loads(json_str)
            elif isinstance(json_str, dict):
                record_dict = json_str
            else:
                raise TypeError(
                    "The JSON object must be str, bytes, bytearray, or dict"
                )
            try:
                permits = [
                    self.dict_to_permit_data(permit) for permit in record_dict["data"]
                ]
            except TypeError as e:
                print(f"An error occurred. {e}")
            else:
                return HistoricalRecord(created=record_dict["created"], data=permits)
        else:
            return HistoricalRecord(created=date.today().isoformat(), data=[])

    def create_application_renewal_history(self):

        historical = ApplicationRenewalHistory.objects.update_or_create(
            application_type=self.application_type,
            application_user=self.application_user,
            process_name=self.process_name,
            defaults={
                "application_type": self.application_type,
                "application_user": self.application_user,
                "process_name": self.process_name,
                "historical_record": historical_record_to_dict(
                    self.prepare_historical_records_to_json()
                ),
            },
        )
        return historical
