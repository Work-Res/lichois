from django_q.tasks import schedule


schedule(
    'gazette.service.tasks.fetch_unread_emails_task.fetch_unread_emails_task',
    schedule_type='I',  # Interval
    minutes=10  # Run every 10 minutes
)
