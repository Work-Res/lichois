from django.db.models.signals import post_save
from django.dispatch import receiver
from .board_meeting import BoardMeeting
from .meeting_invitation import MeetingInvitation
from .board_member import BoardMember


@receiver(post_save, weak=False, sender=BoardMeeting,
          dispatch_uid='board_meeting_on_post_save')
def board_meeting_on_post_save(sender, instance, raw, created, **kwargs):
    """ Create board meeting invitations for all board members when a new board meeting is created.
    """
    if created:
        board_members = BoardMember.objects.filter(board=instance.board_id)
        for member in board_members:
            MeetingInvitation.objects.create(
                meeting_title=instance.title,
                invited_user=member,  # Assuming the board meeting has a 'created_by' field
                status='Pending'
            )
