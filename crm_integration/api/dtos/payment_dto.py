from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class PaymentDTO:
    payment_name: Optional[str]
    amount: Optional[str]
    status: Optional[str]
    payment_ref: Optional[str]
    application_reference: Optional[str]
    service_code: Optional[str]
