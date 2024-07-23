import logging
from django.db import transaction
from django.core.exceptions import ValidationError

from board.models import BoardMember
from citizenship.models import Interview, InterviewQuestion
from citizenship.service.board.score_sheet_service import ScoreSheetService

logger = logging.getLogger(__name__)


class InterviewCompletionService:
    @staticmethod
    @transaction.atomic
    def mark_interview_as_completed(interview_id, member_id):
        try:
            interview = Interview.objects.get(id=interview_id)
            member = BoardMember.objects.get(id=member_id)

            # Check if all interview questions for this member are marked
            all_marked = InterviewQuestion.objects.filter(interview=interview, member=member,
                                                          is_marked=False).count() == 0
            if all_marked:
                interview.completed_by.add(member)
                interview.save()

            # Check if the interview is fully conducted
            all_members_completed = all(
                InterviewQuestion.objects.filter(interview=interview, member=m, is_marked=False).count() == 0
                for m in interview.batch_application.batch.meeting.board.members.all()
            )
            if all_members_completed:
                interview.conducted = True
                interview.save()
                ScoreSheetService.create_score_sheet(interview.id)

            logger.info(f'Interview {interview_id} marked as completed by member {member_id}')
            return interview
        except Interview.DoesNotExist:
            logger.error(f'Interview does not exist: {interview_id}')
            raise ValidationError("Interview does not exist.")
        except BoardMember.DoesNotExist:
            logger.error(f'Member does not exist: {member_id}')
            raise ValidationError("Member does not exist.")
        except Exception as e:
            logger.error(f'Error marking interview as completed: {e}')
            raise ValidationError("Error marking interview as completed.")
