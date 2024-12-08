from django.views.generic import TemplateView
from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact
from app_personal_details.models import (
    Person, Passport, Education, ParentalDetails,
    NextOfKin, Spouse, Child)
from app.models.application_base_model import ApplicationBaseModel
from workresidentpermit.models import (
)EmergencyPermit



new_application = [
    Person,
    Spouse,
    Child,
    ParentalDetails,
    NextOfKin,
    Education,
    Passport,
    ApplicationAddress,
    ApplicationContact,
]

variation = [
    ApplicationBaseModel,
]
