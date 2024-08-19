from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional

from crm_integration.api.dtos import DependentDTO


@dataclass_json
@dataclass
class SubmittedByDTO:
    id: Optional[str]
    type: Optional[str]
    dependent: Optional[DependentDTO]
