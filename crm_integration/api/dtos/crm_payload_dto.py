from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional, List

from crm_integration.api.dtos import CrmDownloadAttachmentDTO


@dataclass_json
@dataclass
class CrmPayloadDTO:
    fields: Optional[List[str]]
    title: Optional[str]
    message: Optional[str]
    description: Optional[str]
    attachments: Optional[List[CrmDownloadAttachmentDTO]]
