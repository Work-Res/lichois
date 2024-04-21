from faker import Faker
from model_mommy.recipe import Recipe

from .models import Application, ApplicationDocument, ApplicationStatus
from .models import ApplicationUser, ApplicationVersion


fake = Faker()

application = Recipe(
    Application,
)

applicationdocument = Recipe(
    ApplicationDocument,
)

applicationstatus = Recipe(
    ApplicationStatus,
)

applicationuser = Recipe(
    ApplicationUser,
)

applicationversion = Recipe(
    ApplicationVersion,
)
