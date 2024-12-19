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

from app_address.admin_site import address_admin
from app_comments.admin_site import comment_admin
from app_contact.admin_site import contact_admin
from app_personal_details.admin_site import personal_details_admin
from authentication.admin_site import authentication_admin
from blue_card.admin_site import blue_card_admin
from board.admin_site import board_admin
from citizenship.admin_site import citizenship_admin
from non_citizen_profile.admin_site import non_citizen_profile_admin
from permanent_residence.admin_site import permanent_residence_admin
from visa.admin_site import visa_admin
from workflow.admin_site import workflow_admin
from workresidentpermit.admin_site import workresidencepermit_admin

new_application = [
        [Person, personal_details_admin],
        [Passport, personal_details_admin],
        [Education, personal_details_admin],
        [ApplicationAddress, address_admin],
        [ApplicationContact, contact_admin],
        [Spouse, personal_details_admin],
        [Child, personal_details_admin],
        [WorkPermit, workresidencepermit_admin],
        [ResidencePermit, workresidencepermit_admin]
]

work_permit = [
    [WorkPermit, workresidencepermit_admin]
]

res_permit = [
    [ResidencePermit, workresidencepermit_admin]
]

work_res_permit = [
    [Person, personal_details_admin],
    [Passport, personal_details_admin],
    [Education, personal_details_admin],
    [ApplicationAddress, address_admin],
    [ApplicationContact, contact_admin],
    [Spouse, personal_details_admin],
    [Child, personal_details_admin],
    [WorkPermit, workresidencepermit_admin],
    [ResidencePermit, workresidencepermit_admin]
]

emergency_permit = [
    [EmergencyPermit, workresidencepermit_admin]
]

exemption_certificate = [
    [Person, personal_details_admin],

    [ExemptionCertificate, workresidencepermit_admin]
]

visa = [
    [VisaApplication, visa_admin],
    [VisaReference, visa_admin]
]

blue_card = [
    [BlueCard, blue_card_admin]
]

variation = [
    [VariationPermit, workresidencepermit_admin]
]

cancellation = [
    [PermitCancellation, workresidencepermit_admin],
]

appeal = [
    [PermitAppeal, workresidencepermit_admin]
]

replacement = [
    [PermitReplacement, workresidencepermit_admin]
]

renewal = new_application[:]
