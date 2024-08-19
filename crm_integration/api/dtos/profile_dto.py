
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class ProfileDTO:
    id: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    surname: Optional[str]
    citizenship: Optional[str]
    date_of_birth: Optional[str]
    gender: Optional[str]
    marital_status: Optional[str]
    employment_status: Optional[str]
    education_level: Optional[str]
    nationality: Optional[str]
    primary_phone: Optional[str]
    primary_postal: Optional[str]
    primary_physical: Optional[str]
    primary_email: Optional[str]
    omang: Optional[str]
    passport: Optional[str]
