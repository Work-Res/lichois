from simple_history.utils import update_change_reason


def update_task_status(task, status, user):
    task.status = status
    task.save()
    task.history.update(history_user=user)
    update_change_reason(task, f"Task status changed to {status}")
