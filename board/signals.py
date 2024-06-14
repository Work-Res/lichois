import logging

from django.dispatch import receiver
from django.db.models.signals import post_save

from board.choices import CANCELLED, ENDED
from board.classes.voting_decision_manager import VotingDecisionManager
from board.models import Agenda, ApplicationBatch, BoardDecision, BoardMeeting, VotingProcess

from workresidentpermit.classes import WorkResidentPermitApplicationDecisionService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BoardDecision)
def create_application_decision(sender, instance, created, **kwargs):
	try:
		if created:
			service = WorkResidentPermitApplicationDecisionService(
				document_number=instance.assessed_application.application_document.document_number,
				board_decision=instance
			)
			service.create()
	except SystemError as e:
		logger.error("SystemError: An error occurred while creating new application decision, Got ", e)
	except Exception as ex:
		logger.error(f"An error occurred while trying to create application decision after saving board decision. "
		             f"Got {ex} ")


@receiver(post_save, sender=VotingProcess)
def create_board_decision(sender, instance, created, **kwargs):
	# if updated then update the board decision
	try:
		if instance.status == ENDED:
			service = VotingDecisionManager(
				document_number=instance.document_number,
				board_meeting=instance.board_meeting
			)
			service.create_board_decision()
	except SystemError as e:
		logger.error("SystemError: An error occurred while creating new board decision, Got ", e)
	except Exception as ex:
		logger.error(f"An error occurred while trying to create board decision after saving voting process. "
		             f"Got {ex} ")


@receiver(post_save, sender=BoardMeeting)
def update_meeting_votes(sender, instance, created, **kwargs):
	try:
		if instance.status == CANCELLED:
			# Get the agenda of the meeting
			agenda = Agenda.objects.filter(meeting=instance).first()
			if agenda:
				app_batch = agenda.application_batch
				batched_applications = app_batch.applications
				for app in batched_applications:
					app.batched = False
					app.save()
				batched_applications.delete()
			# Update the votes of the meeting
	
	except SystemError as e:
		logger.error("SystemError: An error occurred while updating meeting votes, Got ", e)
	except Exception as ex:
		logger.error(f"An error occurred while trying to update meeting votes after saving board meeting. "
		             f"Got {ex} ")
