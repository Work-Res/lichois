import logging
from datetime import datetime

from django.db import transaction

from app.api.common.web import APIMessage, APIResponse
from app_decision.models import ApplicationDecisionType
from workresidentpermit.api.dto.request_dto import RequestDTO


class BaseDecisionService:
	def __init__(self, request: RequestDTO, user=None):
		self.request = request
		self.user = user
		self.logger = logging.getLogger(__name__)
		self.response = APIResponse()
	
	def get_application_decision_type(self):
		try:
			application_decision_type = ApplicationDecisionType.objects.get(
				code__iexact=self.request.status
			)
			return application_decision_type
		except ApplicationDecisionType.DoesNotExist:
			api_message = APIMessage(
				code=400,
				message=f"Application decision provided is invalid: {self.request.status}.",
				details=f"System failed to obtain decision type provided, check if application decision defaults "
				        f"records are created."
			)
			self.response.messages.append(api_message.to_dict())
			return None
	
	@transaction.atomic
	def create_decision(self, decision_model, serializer_class):
		application_decision_type = self.get_application_decision_type()
		if application_decision_type is None:
			return self.response
		
		decision = decision_model.objects.create(
			status=application_decision_type,
			summary=self.request.summary,
			document_number=self.request.document_number,
			approved_by=self.user,
			date_approved=datetime.now()
		)
		
		api_message = APIMessage(
			code=200,
			message="Decision created successfully.",
			details="Decision created successfully."
		)
		self.response.status = "success"
		self.response.data = serializer_class(decision).data
		self.response.messages.append(api_message.to_dict())
		return self.response
	
	def retrieve_decision(self, decision_model, serializer_class):
		try:
			decision = decision_model.objects.get(
				document_number=self.request.document_number
			)
			api_message = APIMessage(
				code=200,
				message="Decision retrieved successfully.",
				details="Decision retrieved successfully."
			)
			self.response.status = "success"
			self.response.data = serializer_class(decision).data
			self.response.messages.append(api_message.to_dict())
			return self.response
		except decision_model.DoesNotExist:
			api_message = APIMessage(
				code=404,
				message="Decision not found.",
				details="No decision found with the provided document number."
			)
			self.response.messages.append(api_message.to_dict())
			self.response.status = "error"
			return self.response
