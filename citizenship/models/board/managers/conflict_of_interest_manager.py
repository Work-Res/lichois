from django.db import models

from ..conflict_of_interest_duration import ConflictOfInterestDuration


class ConflictOfInterestManager(models.Manager):
    def create_conflict(self, attendee, application, meeting_session, has_conflict=True):
        duration = ConflictOfInterestDuration.objects.get(meeting_session=meeting_session)
        if duration.is_within_duration():
            conflict = self.create(
                attendee=attendee,
                application=application,
                has_conflict=has_conflict
            )
            return conflict
        else:
            raise ValueError("Conflicts of interest can only be created within the allowed duration.")
