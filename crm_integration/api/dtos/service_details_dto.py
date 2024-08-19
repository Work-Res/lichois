from dataclasses import dataclass

from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class ServiceDetailsDTO:
    service_id: Optional[str]
    service_name: Optional[str]
    version: Optional[str]
