import uuid

import dateutil.utils
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import BoardDecision, BoardMeeting, Board, Agenda
from .models import BoardMember, InterestDeclaration, MeetingAttendee, AgendaItem

fake = Faker()


agenda = Recipe(
    Agenda
)

agendaitem = Recipe(
    AgendaItem
)

board = Recipe(
    Board,
)

boarddecision = Recipe(
    BoardDecision,
)

boardmeeting = Recipe(
    BoardMeeting,
    id=uuid.uuid4()
)

boardmember = Recipe(
    BoardMember,
    id=uuid.uuid4(),
    board_join_date=dateutil.utils.today()
)

interestdeclaration = Recipe(
    InterestDeclaration,
)

meetingattendee = Recipe(
    MeetingAttendee,
    board_id=uuid.uuid4()
)