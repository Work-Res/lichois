from ..models import Application, Board


class BoardMeetingService:

    def __init__(self, data):
        self.data = data

    def get_board_members(self):

        board_id = self.data.get('attending_board_id')

        try:
            attending_board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return None
        else:
            board_members_id = attending_board.boardmember_set.values_list('id', flat=True)
            return board_members_id

    def get_applications(self):

        application_ids = self.data.get('applications_list')

        application_objs = Application.objects.filter(
            id__in=application_ids)

        return application_objs

