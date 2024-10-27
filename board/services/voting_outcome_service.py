import logging

from django.db.models import Count


from ..choices import ACCEPTED, REJECTED, APPROVED
from ..models import BoardMeetingVote


class VotingOutcomeService:
    def __init__(self, document_number):
        self.document_number = document_number
        self.logger = logging.getLogger(__name__)

    def determine_voting_outcome(self):
        vote_counts = self.get_vote_counts()
        total_approved = vote_counts['APPROVED']
        total_rejected = vote_counts['REJECTED']

        if total_approved == 0 and total_rejected == 0:
            self.logger.error(f"No votes have been cast for {self.document_number}")
            raise ValueError("No votes cast")
        elif total_approved == total_rejected:
            self.logger.info("Chairperson has to break the tie, no board decision")
            raise Exception("Chairperson has to break the tie, no board decision")
        elif total_approved > total_rejected:
            return ACCEPTED
        else:
            return REJECTED

    def get_vote_counts(self):
        vote_counts = (
            BoardMeetingVote.objects.filter(document_number=self.document_number)
            .values('status')
            .annotate(count=Count('status'))
        )

        result = {'APPROVED': 0, 'REJECTED': 0}
        for vote_count in vote_counts:
            if vote_count['status'] == APPROVED.upper():
                result['APPROVED'] = vote_count['count']
            elif vote_count['status'] == REJECTED.upper():
                result['REJECTED'] = vote_count['count']
        return result
