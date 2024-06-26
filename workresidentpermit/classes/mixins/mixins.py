import logging
from workresidentpermit.models import SecurityClearance
from board.models import BoardDecision


class SecurityClearanceMixin:
    def get_security_clearance(self, document_number):
        if not hasattr(self, '_security_clearance') or self._security_clearance is None:
            try:
                self._security_clearance = SecurityClearance.objects.get(document_number=document_number)
            except SecurityClearance.DoesNotExist:
                self.logger = logging.getLogger(__name__)
                self.logger.info(f"Security clearance is pending for {document_number}")
                self._security_clearance = None
        return self._security_clearance


class BoardDecisionMixin:
    def get_board_decision(self, document_number):
        if not hasattr(self, '_board_decision') or self._board_decision is None:
            try:
                self._board_decision = BoardDecision.objects.get(
                    assessed_application__application_document__document_number=document_number
                )
            except BoardDecision.DoesNotExist:
                self.logger = logging.getLogger(__name__)
                self.logger.info(f"Board decision is pending for {document_number}")
                self._board_decision = None
        return self._board_decision
