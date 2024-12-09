from django.views.generic import TemplateView
from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact
from app_personal_details.models import (
    Person, Passport, Education, ParentalDetails,
    NextOfKin, Spouse, Child)
from app.models.application_base_model import ApplicationBaseModel
from workresidentpermit.models import (
    EmergencyPermit,
    ExemptionCertificate,
    PermitAppeal,
    PermitCancellation,
    ResidencePermit,
    WorkPermit,
    Declaration,
    PlaceOfResidence, SpousePlaceOfResidence,
    EmploymentRecord,
    PermitReplacement,
    Dependant,
    PermitCancellationReason,
    VariationPermit
)

new_application = [
    Person,
    Spouse,
    Child,
    ParentalDetails,
    Education,
    Passport,
    ApplicationAddress,
    ApplicationContact,
]

work_permit = [
    WorkPermit
]

res_permit = [
    ResidencePermit
]

work_res_permit = [
     Person,
    Spouse,
    Child,
    ParentalDetails,
    Education,
    Passport,
    ApplicationAddress,
    ApplicationContact,
]

variation = [
    VariationPermit
]

cancellation = [
    PermitCancellation,
    PermitCancellationReason
]

appeal = [
    PermitAppeal
]

replacement = [
    PermitReplacement
]

renewal = new_application[:]
