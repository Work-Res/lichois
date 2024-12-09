from django.views.generic import TemplateView
from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact
from app_personal_details.models import (
    Person, Passport, Education, ParentalDetails,
    NextOfKin, Spouse, Child)
from app.models.application_base_model import ApplicationBaseModel
from visa.models import VisaApplication, VisaReference
from blue_card.models import BlueCard
from citizenship.admin import TravelCertNonCitizenAdmin, TravelCertNonCitizen, TravelCertNonCitizenForm
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
    Education,
    Passport,
    ApplicationAddress,
    ApplicationContact,
    WorkPermit,
    ResidencePermit
]

emergency_permit = [
    EmergencyPermit
]

travel_certificate = [
    TravelCertNonCitizenForm
]

exemption_certificate = [
    ExemptionCertificate
]

visa = [
    VisaApplication,
    VisaReference
]

blue_card = [
    BlueCard
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
