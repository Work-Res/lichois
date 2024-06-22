import logging
from datetime import date

from app.api.common.web import APIResponse, APIMessage
from app.api import NewApplicationDTO
from app.api.serializers import ApplicationVersionSerializer
from app.models import ApplicationDocument, ApplicationUser, ApplicationStatus, Application, ApplicationVersion
from app.utils import ApplicationStatusEnum
from workresidentpermit.classes.document_generator import DocumentGenerator, DocumentGeneratorFactory
from workresidentpermit.classes.work_res_application_repository import ApplicationRepository


class ApplicationService:
	"""
	Service for creating new application records.
	"""
	
	def __init__(self, new_application: NewApplicationDTO):
		self.logger = logging.getLogger(__name__)
		self.application = new_application
		self.response = APIResponse()
		self.application_document = ApplicationDocument()
	
	def create_application(self):
		"""
		Create new application records.
		"""
		if self._is_existing_application():
			return None
		
		application_status = self._get_application_status()
		if not application_status:
			return None
		
		if not self._create_application_document():
			return None
		
		application = self._create_application_record(application_status)
		application_version = self._create_application_version(application)
		
		serializer = ApplicationVersionSerializer(application_version)
		self.response.data = serializer.data
		
		return application_version
	
	def _is_existing_application(self):
		"""
		Check if an application with a new status already exists for the applicant.
		"""
		status = [status.value for status in ApplicationStatusEnum]
		
		existing_application = ApplicationRepository.get_existing_application(
			self.application.applicant_identifier, status
		)
		
		if existing_application.exists():
			self._log_and_set_response(
				400,
				"Bad request",
				f"An application with (NEW) status exists for applicant: {self.application.applicant_identifier}. Complete the existing application before opening a new one."
			)
			return True
		return False
	
	def _get_application_status(self):
		"""
		Get the application status for the current process.
		"""
		try:
			return ApplicationRepository.get_application_status(
				self.application.status, self.application.proces_name
			)
		except ApplicationStatus.DoesNotExist:
			self._log_and_set_response(
				400,
				"Bad request",
				f"Application status ({self.application.status}) does not exist for process name {self.application.proces_name}. User identifier: {self.application.applicant_identifier}"
			)
			return None
	
	def _get_or_create_application_user(self):
		"""
		Create or get an existing application user based on the given user identifier.
		"""
		try:
			user, created = ApplicationRepository.get_or_create_application_user(
				self.application.applicant_identifier,
				{
					"work_location_code": self.application.work_place,
					"dob": self.application.dob,
					"user_identifier": self.application.applicant_identifier,
					"full_name": self.application.full_name
				}
			)
			if created:
				self.logger.info("Created a new application user - %s", self.application.applicant_identifier)
			else:
				self.logger.info("Retrieved existing application user - %s", self.application.applicant_identifier)
			return user
		except Exception as e:
			self._log_and_set_response(
				400,
				"Bad request",
				f"The system failed to create application user with user identifier: {self.application.applicant_identifier}. Error: {e}"
			)
			return None
	
	def _create_application_document(self):
		"""
		Generate the document number for the particular process and create an ApplicationUser.
		"""
		doc_generator = DocumentGeneratorFactory.create_document_generator(self.application)
		document_number = doc_generator.generate_document()
		
		applicant = self._get_or_create_application_user()
		
		if not document_number or not applicant:
			self._log_and_set_response(
				400,
				"Bad request",
				f"The system failed to create application document, document number: {document_number}, applicant: {applicant}."
			)
			return False
		
		self.application_document.document_number = document_number
		self.application_document.applicant = applicant
		self.application_document.document_date = date.today()
		self.application_document.signed_date = date.today()
		ApplicationRepository.save_application_document(self.application_document)
		
		self._log_and_set_response(
			200,
			"Success",
			f"The application has been created with document number: {document_number}."
		)
		return True
	
	def _create_application_record(self, application_status):
		"""
		Create a new application record.
		"""
		application = Application()
		application.application_document = self.application_document
		application.application_status = application_status
		application.process_name = self.application.proces_name
		application.application_type = self.application.application_type
		application.last_application_version_id = 1
		ApplicationRepository.save_application(application)
		return application
	
	def _create_application_version(self, application):
		"""
		Create the initial application version.
		"""
		application_version = ApplicationVersion()
		application_version.application = application
		application_version.version_number = 1
		ApplicationRepository.save_application_version(application_version)
		return application_version
	
	def _log_and_set_response(self, code, message, details):
		"""
		Log the error and set the API response.
		"""
		self.logger.info(details)
		api_message = APIMessage(code=code, message=message, details=details)
		self.response.status = code == 200
		self.response.messages.append(api_message.to_dict())