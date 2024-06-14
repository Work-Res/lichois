from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplicationDTO
from app.classes import CreateNewApplicationService
from app.models import ApplicationStatus
from app.utils import ApplicationProcesses
from app_personal_details.models import Passport, Person
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from faker import Faker
from random import randint

from workresidentpermit.models import EmergencyPermit, ExemptionCertificate


class Command(BaseCommand):
	help = 'Populate data for Populate data for Emergency & Exemption model'
	
	def handle(self, *args, **options):
		faker = Faker()
		for _ in range(50):
			with atomic():
				fname = faker.unique.first_name()
				lname = faker.unique.last_name()
				new_app = NewApplicationDTO(
					application_type='WORK_RES_EXEMPTION_PERMIT',
					process_name=ApplicationProcesses.SPECIAL_PERMIT.name,
					applicant_identifier=f'{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}',
					status='verification',
					dob='1990-06-10',
					work_place=randint(1000, 9999),
					full_name=f'{fname} {lname}'
				)
				self.stdout.write(self.style.SUCCESS('Populating exemption & emergency data...'))
				app = CreateNewApplicationService(new_application=new_app)
				self.stdout.write(self.style.SUCCESS(new_app.__dict__))
				version = app.create()
				Person.objects.get_or_create(
					application_version=version,
					document_number=app.application_document.document_number,
					first_name=fname,
					last_name=lname,
					dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
					middle_name=faker.first_name(),
					marital_status=faker.random_element(elements=('single', 'married', 'divorced')),
					country_birth=faker.country(),
					place_birth=faker.city(),
					gender=faker.random_element(elements=('male', 'female')),
					occupation=faker.job(),
					qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd'))
				)
				country = Country.objects.create(name=faker.country()),
				
				ApplicationAddress.objects.get_or_create(
					application_version=version,
					document_number=app.application_document.document_number,
					po_box=faker.address(),
					apartment_number=faker.building_number(),
					plot_number=faker.building_number(),
					address_type=faker.random_element(elements=('residential', 'postal', 'business', 'private',
					                                            'other')),
					country__id=country[0].id,
					status=faker.random_element(elements=('active', 'inactive')),
					city=faker.city(),
					street_address=faker.street_name(),
					private_bag=faker.building_number(),
				)
				
				ApplicationContact.objects.get_or_create(
					application_version=version,
					document_number=app.application_document.document_number,
					contact_type=faker.random_element(elements=('cell', 'email', 'fax', 'landline')),
					contact_value=faker.phone_number(),
					preferred_method_comm=faker.boolean(chance_of_getting_true=50),
					status=faker.random_element(elements=('active', 'inactive')),
					description=faker.text(),
				)
				
				Passport.objects.get_or_create(
					application_version=version,
					document_number=app.application_document.document_number,
					passport_number=faker.passport_number(),
					date_issued=faker.date_this_century(),
					expiry_date=faker.date_this_century(),
					place_issued=faker.city(),
					nationality=faker.country(),
					photo=faker.image_url(),
				)
				
				ExemptionCertificate.objects.get_or_create(
					document_number=app.application_document.document_number,
					application_version=version,
					business_name=faker.company(),
					employment_capacity=faker.job(),
					proposed_period=randint(1, 12),
					status=faker.random_element(elements=('approved', 'rejected', 'pending')),
					applicant_signature=faker.text(),
					application_date=faker.date_this_century(),
					commissioner_signature=faker.name(),
				)
				
				self.stdout.write(self.style.SUCCESS('Successfully populated data'))
