from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class DependentDTO:
    type: Optional[str]
    id: Optional[str]
