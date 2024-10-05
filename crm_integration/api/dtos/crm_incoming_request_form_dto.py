from dataclasses import dataclass
from dataclasses_json import dataclass_json

from typing import Generic, TypeVar

from crm_integration.api.dtos import PayloadDTO, ReferenceDTO

F = TypeVar('F')


@dataclass_json
@dataclass
class CrmIncomingRequestFormDTO(Generic[F]):
    reference: ReferenceDTO
    payload: PayloadDTO[F]
