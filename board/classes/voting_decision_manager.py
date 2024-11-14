import logging

from app_assessment.models import AssessmentCaseDecision

from app.models import SecurityClearance

from app.service import BaseDecisionService
from app.utils import ApplicationStatusEnum
from app.workflow import ProductionTransactionData
from .dto import BoardDecisionRequestDTO

from ..models import BoardDecision
from ..services import VotingOutcomeService, WorkflowManager


class VotingDecisionManager(BaseDecisionService):

    def __init__(self, document_number, board_meeting, request=None):
        self.document_number = document_number
        self._security_clearance = None
        self._board_decision = None
        self.board_meeting = board_meeting
        self.logger = logging.getLogger(__name__)
        self.voting_outcome_service = VotingOutcomeService(document_number)
        self.board_decision_result_outcome = (
            self.voting_outcome_service.determine_voting_outcome()
        )

        self.workflow = ProductionTransactionData(
            board_decision=self.board_decision_result_outcome.upper(),
            status=self.board_decision_result_outcome.upper(),
        )
        decision_request = BoardDecisionRequestDTO(
            document_number=self.document_number,
            status=self.board_decision_result_outcome,
            board_decision=self.board_decision_result_outcome,
        )
        super().__init__(
            request=request or decision_request,
            workflow=self.workflow,
            task_to_deactivate=ApplicationStatusEnum.VETTING.value,
            application_field_key="recommendation",
        )

    def create_board_decision(self):
        """
        Create or retrieve a BoardDecision for the current document.
        """
        try:
            self.logger.info(
                f"Attempting to retrieve existing BoardDecision for document_number: {self.document_number}"
            )
            self._board_decision = BoardDecision.objects.get(
                document_number=self.document_number
            )
            self.logger.info(
                f"BoardDecision retrieved successfully for document_number: {self.document_number}"
            )

        except BoardDecision.DoesNotExist:
            self.logger.info(
                f"No existing BoardDecision found for document_number: {self.document_number}, creating new one."
            )

            voting_decision_outcome = self.board_decision_result_outcome
            self.logger.info(f"Voting decision outcome: {voting_decision_outcome}")

            if voting_decision_outcome:
                self.logger.info(
                    f"Creating new BoardDecision for document_number: {self.document_number}"
                )
                try:
                    security_object = SecurityClearance.objects.get(
                        document_number=self.document_number
                    )
                except SecurityClearance.DoesNotExist:
                    self.logger.info(
                        f"Security clearance is pending for {self.request.document_number}"
                    )

                try:
                    AssessmentCaseDecision.objects.get(
                        document_number=self.document_number
                    )
                    self.workflow.assessment_obj_exists = True
                except AssessmentCaseDecision.DoesNotExist:
                    self.logger.info(
                        f"Assessment Case Decision is pending for {self.request.document_number}"
                    )

                self._board_decision = BoardDecision.objects.create(
                    document_number=self.document_number,
                    decision_outcome=voting_decision_outcome,
                    board_meeting=self.board_meeting,
                    vetting_outcome=(
                        security_object.status.code.lower() if security_object else "NA"
                    ),
                )
                workflow_manager = WorkflowManager(
                    application=self.application, workflow=self.workflow
                )
                workflow_manager.activate_next_task()
            else:
                self.logger.warning(
                    f"Voting decision outcome is None for document_number: {self.document_number}. "
                    f"No BoardDecision created."
                )
        except Exception:
            self.logger.error(
                f"An error occurred while creating or retrieving BoardDecision for document_number: {self.document_number}",
                exc_info=True,
            )
        finally:
            return self._board_decision

    # def _activate_next_task(self):
    #     """
    #     Activate the next task in the workflow if a workflow and decision are specified.
    #     """
    #     try:
    #         if self.workflow:
    #
    #             # Log the decision and workflow details
    #             self.logger.info(f"Workflow: {self.workflow}, Decision: {self.decision}")
    #
    #             # Log the task signal creation
    #             self.logger.info(f"Creating or updating task for application: {self.application}")
    #             create_or_update_task_signal.send_robust(
    #                 sender=self.application,
    #                 source=self.workflow,
    #                 application=self.application,
    #             )
    #             self.logger.info("Task signal sent successfully.")
    #         else:
    #             self.logger.warning(
    #                 f"Cannot activate next task. Workflow({self.workflow}) or decision{self.decision} is missing.")
    #
    #     except Exception as e:
    #         self.logger.error(f"Error occurred while activating next task: {str(e)}")
    #         raise
