from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.models import ApplicationStatus
from app.utils import ApplicationProcesses
from app.utils.system_enums import ApplicationStatusEnum
from app_personal_details.models import Passport, Person
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from faker import Faker
from random import randint

from workresidentpermit.models import EmergencyPermit, ExemptionCertificate, PermitAppeal
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(BaseCommand):
	help = 'Populate data for Populate data for Emergency & Exemption model'
	
	def handle(self, *args, **options):
		faker = Faker()
		process_name = ApplicationProcesses.SPECIAL_PERMIT.name
		self.stdout.write(self.style.SUCCESS(f'Process name {process_name}'))
		ApplicationStatus.objects.get_or_create(
			code=ApplicationStatusEnum.NEW.value,
			name=ApplicationStatusEnum.VERIFICATION.name,
			processes=f'{process_name}, {ApplicationProcesses.WORK_RESIDENT_PERMIT.name}, '
			          f'{ApplicationProcesses.WORK_PERMIT.name}, {ApplicationProcesses.RESIDENT_PERMIT.name}',
			valid_from='2024-01-01',
			valid_to='2026-12-31',
		)
		ApplicationStatus.objects.get_or_create(
			code=ApplicationStatusEnum.VERIFICATION.value,
			name=ApplicationStatusEnum.VERIFICATION.name,
			processes=f'{process_name}, {ApplicationProcesses.WORK_RESIDENT_PERMIT.name}, '
			          f'{ApplicationProcesses.WORK_PERMIT.name}, {ApplicationProcesses.RESIDENT_PERMIT.name}',
			valid_from='2024-01-01',
			valid_to='2026-12-31',
		)
		
		for _ in range(150):
			fname = faker.unique.first_name()
			lname = faker.unique.last_name()
			with atomic():
				new_app = NewApplicationDTO(
					application_type=WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_APPEAL.name,
					process_name=process_name,
					applicant_identifier=f'{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}',
					status=ApplicationStatusEnum.VERIFICATION.value,
					dob='1990-06-10',
					work_place=randint(1000, 9999),
					full_name=f'{fname} {lname}',
				)
				self.stdout.write(self.style.SUCCESS('Populating appeal data...'))
				app = ApplicationService(new_application=new_app)
				self.stdout.write(self.style.SUCCESS(new_app.__dict__))
				version = app.create_application()
				Person.objects.get_or_create(
					application_version=version,
					first_name=fname,
					last_name=lname,
					document_number=app.application_document.document_number,
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
				
				PermitAppeal.objects.get_or_create(
					application_version=version,
					document_number=app.application_document.document_number,
					appeal_type=faker.random_element(elements=('appeal', 'review', 'renewal', 'reconsideration')),
					reason_for_appeal=faker.text(),
					appeal_date=faker.date_this_century(),
				)
				
				self.stdout.write(self.style.SUCCESS('Successfully populated data'))
