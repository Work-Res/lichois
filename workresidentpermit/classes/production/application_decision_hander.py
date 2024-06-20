import logging
from app.models import Application
from app.utils import ApplicationDecisionEnum
from app_decision.models import ApplicationDecision
from ...api.dto import PermitRequestDTO
from ...classes.service import PermitProductionService

logger = logging.getLogger(__name__)


class ApplicationDecisionHandler:
	def __init__(self,  permit_service_class):
		self.permit_service_class = permit_service_class
	
	def handle(self, instance: ApplicationDecision):
		"""Handle the decision logic and create a production permit record if necessary."""
		try:
			if instance.proposed_decision_type.code == ApplicationDecisionEnum.ACCEPTED.value:
				application = Application.objects.get(application_document__document_number=instance.document_number)
				if self._requires_permit(application):
					request = self._build_permit_request(instance, application)
					permit_service = self.permit_service_class(request=request)
					permit_service.create_new_permit()
		except SystemError as e:
			logger.error(
				f"SystemError: An error occurred while creating permit for production {instance.document_number}, Got {e}")
		except Exception as ex:
			logger.error(
				f"An error occurred while trying to create permit for production {instance.document_number}. Got {ex}")
	
	@staticmethod
	def _requires_permit(application: Application) -> bool:
		"""Check if the application process requires a permit."""
		# This could be made more dynamic by checking the process name against a list of permit processes
		return application.process_name.upper() == "WORK_RESIDENT_PERMIT"
	
	@staticmethod
	def _build_permit_request(instance: ApplicationDecision, application: Application) -> PermitRequestDTO:
		"""Build the permit request DTO."""
		request = PermitRequestDTO()
		request.permit_type = application.process_name
		request.place_issue = "Gaborone"  # This could be made dynamic
		request.document_number = instance.document_number
		return request
