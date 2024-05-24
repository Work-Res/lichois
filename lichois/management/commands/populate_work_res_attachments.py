import random

from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplication
from app.classes import CreateNewApplication
from app.models import Application, ApplicationDocument, ApplicationStatus
from app_attachments.models import ApplicationAttachment, ApplicationAttachmentVerification, AttachmentDocumentType
from app_personal_details.models import Passport, Person
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from faker import Faker
from random import randint

from authentication.models import User
from workresidentpermit.models import ResidencePermit, WorkPermit


class Command(BaseCommand):
	help = 'Populate data for Work & Res Application model'
	
	def handle(self, *args, **options):
		faker = Faker()
		apps = ApplicationDocument.objects.all()
		verifier = User.objects.filter(username='tverification1').first()
		for app in apps:
			for _ in range(randint(3, 6) + 1):
				document_type = AttachmentDocumentType.objects.create(
					code=faker.random_int(min=1000, max=9999),
					name=faker.random_element(elements=('passport', 'national_id', 'birth_certificate')),
					valid_from=faker.date_this_decade(),
					valid_to=faker.date_this_decade(),
				)
				attachment = ApplicationAttachment.objects.create(
					filename=faker.file_name(),
					storage_object_key=faker.file_name(),
					description=faker.sentence(),
					document_url='https://s2.q4cdn.com/175719177/files/doc_presentations/Placeholder-PDF.pdf',
					received_date=faker.date_time_this_decade(),
					document_type=document_type,
					document_number=app.document_number
				)
				ApplicationAttachmentVerification.objects.create(
					attachment=attachment,
					verification_status=faker.random_element(elements=('pending', 'approved', 'rejected')),
					verifier=verifier,
				)
	
	def get_random_file_extension(self, category):
		file_extensions = {
			'pdf': ['.pdf'],
			'image': ['.jpg', '.png', '.gif'],
			'text': ['.txt', '.doc', '.docx'],
			# Add more categories and file extensions as needed
		}
		
		return random.choice(file_extensions.get(category, []))