from typing import List

from dataclasses import dataclass, asdict

from app_personal_details.models import PermitData


@dataclass
class HistoricalRecord:

    created: str
    data: List[PermitData]


def permit_data_to_dict(permit_data: PermitData) -> dict:
    return {
        'permit_type': permit_data.permit_type,
        'permit_no': permit_data.permit_no,
        'date_issued': permit_data.date_issued.isoformat(),
        'date_expiry': permit_data.date_expiry.isoformat(),
        'place_issue': permit_data.place_issue,
        'document_number': permit_data.document_number
    }


def historical_record_to_dict(historical_record: HistoricalRecord) -> dict:
    record_dict = asdict(historical_record)
    record_dict['data'] = [permit_data_to_dict(permit) for permit in historical_record.data]
    return record_dict
