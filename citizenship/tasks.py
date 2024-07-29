from django.utils import timezone
from django_q.tasks import schedule

from citizenship.models.board.conflict_of_interest_duration import ConflictOfInterestDuration


def check_conflict_of_interest_duration():
    current_time = timezone.now()

    # Start the duration
    pending_durations = ConflictOfInterestDuration.objects.filter(start_time__lte=current_time, status='pending')
    for duration in pending_durations:
        duration.status = 'open'
        duration.save()
        print(f"Duration for session {duration.meeting_session} is now open.")

    # End the duration
    open_durations = ConflictOfInterestDuration.objects.filter(end_time__lte=current_time, status='open')
    for duration in open_durations:
        duration.status = 'completed'
        duration.save()
        print(f"Duration for session {duration.meeting_session} is now completed.")


schedule(
    'citizenship.tasks.check_conflict_of_interest_duration',
    schedule_type='I',  # Interval-based scheduling
    minutes=2
)
