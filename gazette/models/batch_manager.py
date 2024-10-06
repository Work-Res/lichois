from django.db import models


class BatchManager(models.Manager):
    def get_or_create_by_status(self, title, description, status='IN_PROGRESS', date_of_publish=None, identifier=None):
        batch, created = self.get_or_create(
            status=status,
            defaults={
                'title': title,
                'description': description,
                'date_of_publish': date_of_publish,
                'identifier': identifier
            }
        )
        return batch, created
