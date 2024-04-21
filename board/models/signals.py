from django.db.models.signals import post_save
from django.dispatch import receiver
from .board_meeting import BoardMeeting
from .board import Board
from .meeting_attendee import MeetingAttendee


@receiver(post_save, weak=False, sender=BoardMeeting,
          dispatch_uid='board_meeting_on_post_save')
def board_meeting_on_post_save(sender, instance, raw, created, **kwargs):
    """ Create board meeting attendees upon creation of board meeting
    """

    board_id = instance.board_id
    board_members = None

    try:
        attending_board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        return None
    else:
        board_members = attending_board.boardmember_set.all()

    for board_member in board_members:

        MeetingAttendee.objects.update_or_create(
            meeting=instance,
            board_member=board_member)
