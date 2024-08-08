from faker import Faker
from model_mommy.recipe import Recipe

from .models import AdoptedChildRegistration, CertNaturalisationByForeignSpouse, CitizenSponsorCertificate
from .models import CitizenshipBySettlement, CitizenshipRenunciationDeclaration, CitizenshipResumption
from .models import DCCertificate, DeclarationNaturalisationByForeignSpouse, DoubtCitizenshipCertificate
from .models import KgosiCertificate, KgosanaCertificate, LateCitizenshipRenunciation
from .models import MaturityPeriodWaiver, NationalityDeclaration, Naturalisation, OathOfAllegiance
from .models import RenunciationOfForeignCitizenship, ParentDetails, PersonalDeclaration
from .models import PlaceOfResidence, PresidentPower10A, PresidentPower10B, ResidentialHistory
from .models import SpouseInfo, TravelCertNonCitizen, Under20Citizenship


fake = Faker()

adoptedchildregistration = Recipe(
    AdoptedChildRegistration,
)

under20citizenship = Recipe(
    Under20Citizenship,
)

certnaturalisationbyforeignspouse = Recipe(
    CertNaturalisationByForeignSpouse,
)

renunciationofforeigncitizenship = Recipe(
    RenunciationOfForeignCitizenship,
)

maturityperiodwaiver = Recipe(
    MaturityPeriodWaiver,
)

presidentpower10b = Recipe(
    PresidentPower10B,
)

kgosicertificate = Recipe(
    KgosiCertificate,
)

kgosanacertificate = Recipe(
    KgosanaCertificate,
)

dccertificate = Recipe(
    DCCertificate,
)


