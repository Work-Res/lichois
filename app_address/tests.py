from django.test import TestCase

# Create your tests here.
from model_mommy import mommy
from .models import Application, ApplicationDocument, ApplicationStatus

# Assuming you have models ApplicationDocument and ApplicationStatus defined similarly to Application
# Create a sample ApplicationDocument
application_document = mommy.make(ApplicationDocument)

# Create a sample ApplicationStatus
application_status = mommy.make(ApplicationStatus)

# Create a sample Application
application = mommy.make(
    Application,
    application_document=application_document,
    application_status=application_status,
    last_application_version_id=1  # You may adjust this value as needed
)
