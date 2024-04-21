from faker import Faker
from model_mommy.recipe import Recipe

from .models import BlueCardApplication, BlueCard, ContactMethod
from .models import DisposalMoney, ExemptionCertificate, ExemptionCertificateDependant
from .models import ExemptionCertificateApplication, VisaApplication, Visa
from .models import VisaReference

fake = Faker()

bluecardapplication = Recipe(
    BlueCardApplication,
)

bluecard = Recipe(
    BlueCard,
)

contactmethod = Recipe(
    ContactMethod,
)

disposalmoney = Recipe(
    DisposalMoney,
)

exemptioncertificate = Recipe(
    ExemptionCertificate,
)

exemptioncertificatedependant = Recipe(
    ExemptionCertificateDependant,
)

exemptioncertificateapplication = Recipe(
    ExemptionCertificateApplication,
)

visaapplication = Recipe(
    VisaApplication,
)

visa = Recipe(
    Visa,
)

visareference = Recipe(
    VisaReference,
)
