from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional

from crm_integration.api.dtos import ProfileDTO, ServiceDetailsDTO, SubmittedByDTO


@dataclass_json
@dataclass
class ReferenceDTO:
    profile: Optional[ProfileDTO]
    service: Optional[ServiceDetailsDTO]
    submitted_by: Optional[SubmittedByDTO]
    status: Optional[str]
    application_id: Optional[str]
    submission_id: Optional[str]
    response_id: Optional[str]
