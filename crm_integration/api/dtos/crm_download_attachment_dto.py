from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class CrmDownloadAttachmentDTO:
    name: Optional[str]
    bucket_id: Optional[str]
    key: Optional[str]
    original_name: Optional[str]
    extension: Optional[str]
