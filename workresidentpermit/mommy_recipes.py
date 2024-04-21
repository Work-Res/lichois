from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import Child, EmergencyResPermitApplication, EmergencyResidencePermit
from .models import ExemptionCertificate, Permit, ResidencePermitAppeal
from .models import ResidencePermitCancellation, Spouse, WorkResidencePermit

fake = Faker()

child = Recipe(
    Child,
)

emergencyrespermitapplication = Recipe(
    EmergencyResPermitApplication,
)

emergencyresidencepermit = Recipe(
    EmergencyResidencePermit,
)

exemptioncertificate = Recipe(
    ExemptionCertificate,
)

permit = Recipe(
    Permit,
)

residencepermitappeal = Recipe(
    ResidencePermitAppeal,
)

residencepermitcancellation = Recipe(
    ResidencePermitCancellation,
)

spouse = Recipe(
    Spouse,
)

workresidencepermit = Recipe(
    WorkResidencePermit,
)
