import logging
from django.db import transaction
from django.core.exceptions import ValidationError
from citizenship.models.board import InterviewDecision, Interview, BoardMember

logger = logging.getLogger(__name__)


class InterviewDecisionService:
    @staticmethod
    @transaction.atomic
    def create_decision(interview_id, member_id, passed, reason=''):
        try:
            interview = Interview.objects.get(id=interview_id)
            member = BoardMember.objects.get(id=member_id)
            if not passed and not reason:
                raise ValidationError("Reason is required when the decision is not passed.")
            decision = InterviewDecision.objects.create(
                interview=interview,
                member=member,
                passed=passed,
                reason=reason
            )
            logger.info(f'Decision created: {decision}')
            return decision
        except Interview.DoesNotExist:
            logger.error(f'Interview does not exist: {interview_id}')
            raise ValidationError("Interview does not exist.")
        except BoardMember.DoesNotExist:
            logger.error(f'Member does not exist: {member_id}')
            raise ValidationError("Member does not exist.")
        except Exception as e:
            logger.error(f'Error creating decision: {e}')
            raise ValidationError("Error creating decision.")

    @staticmethod
    def get_decision(decision_id):
        try:
            decision = InterviewDecision.objects.get(id=decision_id)
            logger.info(f'Decision retrieved: {decision}')
            return decision
        except InterviewDecision.DoesNotExist:
            logger.error(f'Decision does not exist: {decision_id}')
            raise ValidationError("Decision does not exist.")

    @staticmethod
    @transaction.atomic
    def update_decision(decision_id, passed=None, reason=None):
        try:
            decision = InterviewDecision.objects.get(id=decision_id)
            if passed is not None:
                decision.passed = passed
            if reason is not None:
                if not passed and not reason:
                    raise ValidationError("Reason is required when the decision is not passed.")
                decision.reason = reason
            decision.save()
            logger.info(f'Decision updated: {decision}')
            return decision
        except InterviewDecision.DoesNotExist:
            logger.error(f'Decision does not exist: {decision_id}')
            raise ValidationError("Decision does not exist.")
        except Exception as e:
            logger.error(f'Error updating decision: {e}')
            raise ValidationError("Error updating decision.")

    @staticmethod
    @transaction.atomic
    def delete_decision(decision_id):
        try:
            decision = InterviewDecision.objects.get(id=decision_id)
            decision.delete()
            logger.info(f'Decision deleted: {decision}')
            return True
        except InterviewDecision.DoesNotExist:
            logger.error(f'Decision does not exist: {decision_id}')
            raise ValidationError("Decision does not exist.")
        except Exception as e:
            logger.error(f'Error deleting decision: {e}')
            raise ValidationError("Error deleting decision.")
