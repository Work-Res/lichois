from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.utils import ApplicationProcesses
from app.utils.system_enums import ApplicationStatusEnum
from app_personal_details.models import Passport, Person
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from faker import Faker
from random import randint

from workresidentpermit.models import ExemptionCertificate
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum


class Command(BaseCommand):
	help = 'Populate data for Populate data for Emergency & Exemption model'
	
	def handle(self, *args, **options):
		faker = Faker()
		process_name = ApplicationProcesses.EXEMPTION_CERTIFICATE.value
		
		for _ in range(250):
			with atomic():
				fname = faker.unique.first_name()
				lname = faker.unique.last_name()
				application_type = faker.random_element(elements=(
					# WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE.value,
					WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_APPEAL.value,
					WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_RENEWAL.value,
					WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_REPLACEMENT.value,
					WorkResidentPermitApplicationTypeEnum.EXEMPTION_CERTIFICATE_CANCELLATION.value,
				))
				new_app = NewApplicationDTO(
					application_type=application_type,
					process_name=process_name,
					applicant_identifier=f'{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}',
					status=ApplicationStatusEnum.VERIFICATION.value,
					dob='1990-06-10',
					work_place=randint(1000, 9999),
					full_name=f'{fname} {lname}'
				)
				self.stdout.write(self.style.SUCCESS('Populating exemption data...'))
				app = ApplicationService(new_application=new_app)
				version = app.create_application()
				self.stdout.write(self.style.SUCCESS(f'version data... {version}'))
				self.stdout.write(self.style.SUCCESS(app.application_document.document_number))
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
