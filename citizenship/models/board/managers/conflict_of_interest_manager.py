from django.db import models

from ..conflict_of_interest_duration import ConflictOfInterestDuration


class ConflictOfInterestManager(models.Manager):
    def create_conflict(self, attendee, application, meeting_session, has_conflict=True,
                        client_relationship=None, interest_description=None):
        duration = ConflictOfInterestDuration.objects.get(meeting_session=meeting_session)
        if duration.is_within_duration():
            conflict = self.create(
                attendee=attendee,
                application=application,
                has_conflict=has_conflict,
                client_relationship=client_relationship,
                interest_description=interest_description
            )
            return conflict
        else:
            raise ValueError("Conflicts of interest can only be created within the allowed duration.")
