import logging
from django.utils import timezone

from datetime import datetime, time
from datetime import timedelta

from app_checklist.models import Holiday


class MeetingSessionService:
    def __init__(self, meeting_session):
        self.meeting_session = meeting_session
        self.meeting_session_model = meeting_session._meta.model

    def generate_recurring_sessions(self):

        meeting = self.meeting_session.meeting
        current_date = timezone.make_aware(datetime.combine(self.meeting_session.date, time.min))
        sessions = []
        while current_date <= meeting.end_date:
            current_date += timedelta(days=1)
            # Check if the current_date is a weekend (Saturday or Sunday)
            if self.meeting_session.skip_weekend and current_date.weekday() >= 5:
                logging.info(f"Skipping {current_date} as it is a weekend.")
            # Check if the current_date is a holiday
            elif self.meeting_session.skip_holiday and Holiday.objects.filter(
                    holiday_date=current_date).exists():
                logging.info(f"Skipping {current_date} as it is a holiday.")
            else:
                session = self.meeting_session_model.objects.create(
                    meeting=meeting,
                    title=self.meeting_session.title,
                    date=current_date,
                    start_time=self.meeting_session.start_time,
                    end_time=self.meeting_session.end_time,
                    batch_application_complete=self.meeting_session.batch_application_complete,
                )
                sessions.append(session)

        return sessions

    def generate_sessions_for_custom_dates(self, custom_dates):
        """
        Generates meeting sessions for the provided custom dates.

        :param custom_dates: List of dates (datetime.date objects) for which to create sessions.
        :return: List of created MeetingSession objects.
        """
        sessions = []
        for custom_date in custom_dates:
            session = self.meeting_session_model.objects.create(
                meeting=self.meeting_session.meeting,
                title=self.meeting_session.title,
                date=custom_date,
                start_time=self.meeting_session.start_time,
                end_time=self.meeting_session.end_time,
                batch_application_complete=self.meeting_session.batch_application_complete,
            )
            sessions.append(session)
        return sessions
