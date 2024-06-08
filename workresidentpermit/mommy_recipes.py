from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import Child, EmergencyResPermitApplication, EmergencyPermit, PermitCancellation
from .models import ExemptionCertificate, Permit, PermitAppeal
from .models import Spouse, WorkResidencePermit

fake = Faker()

child = Recipe(
    Child,
)

emergencyrespermitapplication = Recipe(
    EmergencyResPermitApplication,
)

emergencyresidencepermit = Recipe(
    EmergencyPermit,
)

exemptioncertificate = Recipe(
    ExemptionCertificate,
)

permit = Recipe(
    Permit,
)

residencepermitappeal = Recipe(
    PermitAppeal,
)

residencepermitcancellation = Recipe(
    PermitCancellation,
)

spouse = Recipe(
    Spouse,
)

workresidencepermit = Recipe(
    WorkResidencePermit,
)
