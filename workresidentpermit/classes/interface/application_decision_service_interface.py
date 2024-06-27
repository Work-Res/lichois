import logging
from abc import ABC, abstractmethod
from django.db import transaction

from app.models import Application


class IApplicationDecisionService(ABC):
	@abstractmethod
	def decision_predicate(self) -> bool:
		pass
	
	@abstractmethod
	@transaction.atomic
	def create_application_decision(self):
		pass
	
	@abstractmethod
	def run_workflow(self, application: Application, workflow):
		pass
