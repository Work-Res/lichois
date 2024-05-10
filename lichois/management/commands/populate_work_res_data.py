from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from app.api import NewApplication
from app.classes import CreateNewApplication
from app.models import ApplicationStatus
from app_address.choices import ADDRESS_TYPE
from app_contact.models.choices import CONTACT_TYPES
from app_personal_details.models import Passport, Person
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from faker import Faker
from random import randint

from workresidentpermit.choices import REASONS_PERMIT, YES_NO
from workresidentpermit.models import ResidencePermit, WorkPermit
from base_module.choices import PERMIT_STATUS


class Command(BaseCommand):
	help = 'Populate data for Work & Res Application model'
	
	def handle(self, *args, **options):
		faker = Faker()
		ApplicationStatus.objects.get_or_create(
			code='new',
			name='New',
			processes='work',
			valid_from='2024-01-01',
			valid_to='2026-12-31',
		)
		
		for _ in range(5):
			with atomic():
				new_app = NewApplication(
					process_name='WORK_RESIDENT_PERMIT',
					applicant_identifier=f'{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}',
					status='new',
					dob='1990-06-10',
					work_place=faker.company(),
					full_name=faker.name(),
				)
				self.stdout.write(self.style.SUCCESS('Populating data...'))
				self.stdout.write(self.style.SUCCESS(f'New Application: {new_app.applicant_identifier}'))
				app = CreateNewApplication(new_application=new_app)
				version = app.create()
				self.stdout.write(self.style.SUCCESS(f'Application Version: {version.__dict__}'))
				Person.objects.get_or_create(
					application_version__application__application_document__document_number=app.application_document.document_number,
					first_name=faker.unique.first_name(),
					last_name=faker.unique.last_name(),
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
				coun = country[0]
				temp = Country.objects.filter(name=faker)
				self.stdout.write(self.style.SUCCESS(f'New country: {coun}'))
				ApplicationAddress.objects.get_or_create(
					application_version__application__application_document__document_number=app.application_document
					.document_number,
					po_box=faker.address(),
					apartment_number=faker.building_number(),
					plot_number=faker.building_number(),
					address_type=faker.random_element(elements=ADDRESS_TYPE),
					country__id=coun.id,
					status=faker.random_element(elements=('active', 'inactive')),
					city=faker.city(),
					street_address=faker.street_name(),
					private_bag=faker.building_number(),
				)
				
				ApplicationContact.objects.get_or_create(
					application_version__application__application_document__document_number=app.application_document
					.document_number,
					contact_type=faker.random_element(elements=CONTACT_TYPES),
					contact_value=faker.phone_number(),
					preferred_method_comm=faker.boolean(chance_of_getting_true=50),
					status=faker.random_element(elements=('active', 'inactive')),
					description=faker.text(),
				)
				
				Passport.objects.get_or_create(
					application_version__application__application_document__document_number=app.application_document
					.document_number,
					passport_number=faker.passport_number(),
					date_issued=faker.date_this_century(),
					expiry_date=faker.date_this_century(),
					place_issued=faker.city(),
					nationality=faker.country(),
					photo=faker.image_url(),
				)
				
				ResidencePermit.objects.get_or_create(
					application_version__application__application_document__document_number=app.application_document
					.document_number,
					language=faker.language_code(),
					permit_reason=faker.text(),
					previous_nationality=faker.country(),
					current_nationality=faker.country(),
					state_period_required=faker.date_this_century(),
					propose_work_employment=faker.random_element(elements=YES_NO),
					reason_applying_permit=faker.random_element(elements=REASONS_PERMIT),
					documentary_proof=faker.text(),
					travelled_on_pass=faker.text(),
					is_spouse_applying_residence=faker.random_element(elements=YES_NO),
					ever_prohibited=faker.text(),
					sentenced_before=faker.text(),
					entry_place=faker.city(),
					arrival_date=faker.date_this_century(),
				)
				
				WorkPermit.objects.get_or_create(
					application_version__application__application_document__document_number=app.application_document
					.document_number,
					permit_status=faker.random_element(elements=PERMIT_STATUS),
					job_offer=faker.text(),
					qualification=faker.text(),
					years_of_study=faker.random_int(min=1, max=10),
					business_name=faker.company(),
					type_of_service=faker.text(),
					job_title=faker.job(),
					job_description=faker.text(),
					renumeration=faker.random_int(min=10000, max=100000),
					period_permit_sought=faker.random_int(min=1, max=10),
					has_vacancy_advertised=faker.boolean(chance_of_getting_true=50),
					have_funished=faker.boolean(chance_of_getting_true=50),
					reasons_funished=faker.text(),
					time_fully_trained=faker.random_int(min=1, max=10),
					reasons_renewal_takeover=faker.text(),
					reasons_recruitment=faker.text(),
					labour_enquires=faker.text(),
					no_bots_citizens=faker.random_int(min=1, max=10),
					name=faker.name(),
					educational_qualification=faker.text(),
					job_experience=faker.text(),
					take_over_trainees=faker.text(),
					long_term_trainees=faker.text(),
					date_localization=faker.date_this_century(),
					employer=faker.company(),
					occupation=faker.job(),
					duration=faker.random_int(min=1, max=10),
					names_of_trainees=faker.text(),
				)
				self.stdout.write(self.style.SUCCESS('Successfully populated data'))
