from citizenship.models import ConflictOfInterest, ConflictOfInterestDuration, BoardMember, Attendee, MeetingSession


class ConflictOfInterestValidator:

    def __init__(self, document_number, attendee_id, meeting_session):
        self.document_number = document_number
        self.attendee_id = attendee_id
        self.meeting_session_id = meeting_session

    def meeting_session(self):
        return MeetingSession.objects.get(id=self.meeting_session_id)

    def is_eligible_to_declare_conflict_of_interest(self):
        meeting_session = self.meeting_session()
        reasons = []
        if not self.has_conflict_of_interest_duration_started():
            reasons.append(
                f"Conflict of interest duration has not started for the meeting session. "
                f"Start date: {meeting_session.start_date}, End date: {meeting_session.end_date}."
            )

        if self.has_declared_conflict_of_interest():
            reasons.append(
                f"Attendee {self.attendee_id} has already declared a conflict of interest for document "
                f"{self.document_number}."
            )

        if not self.is_attendee_a_board_member():
            reasons.append(
                f"Attendee {self.attendee_id} is not linked to any board member. Please confirm if the attendee ID is"
                f" correct."
            )

        return reasons if reasons else None

    def has_declared_conflict_of_interest(self):
        return ConflictOfInterest.objects.filter(
            application__application_document__document_number=self.document_number,
            attendee__member__user=self.attendee_id
        ).exists()

    def has_conflict_of_interest_duration_started(self):
        return ConflictOfInterestDuration.objects.filter(
            meeting_session=self.meeting_session()
        ).exists()

    def is_attendee_a_board_member(self):
        return Attendee.objects.filter(member__user__id=self.attendee_id.id).exists()
