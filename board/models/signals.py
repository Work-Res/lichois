from django.db.models.signals import post_save
from django.dispatch import receiver

from . import Board, MeetingAttendee
from .board_meeting import BoardMeeting
from .meeting_invitation import MeetingInvitation


@receiver(post_save, weak=False, sender=BoardMeeting,
          dispatch_uid='board_meeting_on_post_save')
def board_meeting_on_post_save(sender, instance, raw, created, **kwargs):
    """ Create board meeting invitations for all board members when a new board meeting is created.
    """
    if created:
        board_id = instance.board_id
        board_members = None
        
        try:
            attending_board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return None
        else:
            board_members = attending_board.boardmember_set.all()
            for board_member in board_members:
                # Create a meeting invitation for each board member
                MeetingInvitation.objects.create(
                    board_meeting=instance,
                    invited_user=board_member,
                )
            
        
@receiver(post_save, weak=False, sender=MeetingInvitation,
          dispatch_uid='board_meeting_invitation_on_post_save')
def board_meeting_invitation_on_post_save(sender, instance, raw, created, **kwargs):
    attendance_status = 'present' if instance.status == 'approved' else 'absent'
    MeetingAttendee.objects.update_or_create(
        meeting=instance.board_meeting,
        board_member=instance.user_invited,
        attendance_status=attendance_status
    )


