from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Generic, TypeVar, Optional, List

from crm_integration.api.dtos import PaymentDTO

F = TypeVar('F')


@dataclass_json
@dataclass
class PayloadDTO(Generic[F]):
    form: Optional[F]
    payment: Optional[PaymentDTO]
    attachments: Optional[List[str]]
