from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from model_mommy import mommy
from app.api import NewApplication
from app.classes import CreateNewApplication
from app.models import ApplicationStatus
from app_personal_details.models import Person
from app_address.models import ApplicationAddress, Country
from workresidentpermit.classes import WorkResidentPermitData
from faker import Faker
from random import randint


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
				self.stdout.write(self.style.SUCCESS(f'New Application: {new_app.work_place}'))
				new_app = CreateNewApplication(new_application=new_app)
				version = new_app.create()
				self.stdout.write(self.style.SUCCESS(f'Application Version: {version.__dict__}'))
				Person.objects.get_or_create(
					application_version__application__application_document__document_number=new_app.application_document.document_number,
					first_name=faker.first_name(),
					last_name=faker.last_name(),
					dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
					middle_name=faker.first_name(),
					marital_status=faker.random_element(elements=('single', 'married', 'divorced')),
					country_birth=faker.country(),
					place_birth=faker.city(),
					gender=faker.random_element(elements=('male', 'female')),
					occupation=faker.job(),
					qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd'))
				)
				
				ApplicationAddress.objects.get_or_create(
					application_version__application__application_document__document_number=new_app.application_document.document_number,
					postal_address=faker.address(),
					physical_address=faker.address(),
					phone_number=faker.phone_number(),
					apartment_number=faker.building_number(),
					plot_number=faker.building_number(),
					country=Country.objects.get_or_create(
						name=faker.country(),
						valid_from='2024-01-01',
						valid_to='2026-12-31',
					),
					status=faker.random_element(elements=('active', 'inactive')),
					city=faker.city(),
					street_address=faker.street_name(),
					address_type=faker.random_element(elements=('private', 'postal')),
					private_bag=faker.building_number(),
					version=version,
				)
				
				self.stdout.write(self.style.SUCCESS('Successfully populated data'))
