from django.db import models


class BoardBasePermissionModel(models.Model):
    class Meta:
        abstract = True
        permissions = [
            ('can_update_board_decision', 'Can update Board Decision'),
            ('can_delete_board_decision', 'Can delete Board Decision'),
            ('can_view_board_decision', 'Can view Board Decision'),
            ('can_view_board_vote', 'Can view board vote'),
            ('can_delete_board_vote', 'Can delete board vote'),
            ('can_update_board_vote', 'Can update board vote'),
            ('can_delete_conflict_of_interest', 'Can delete conflict of interest'),
            ('can_view_conflict_of_interest', 'Can view conflict of interest'),
            ('can_update_conflict_of_interest', 'Can view conflict of interest'),
            ('can_board_attendee', 'Can board attendee'),
            ('can_view_board_attendee', 'Can view board attendee'),
            ('can_delete_board_attendee', 'Can delete board attendee'),
        ]
