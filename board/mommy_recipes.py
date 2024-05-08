import uuid

import dateutil.utils
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import BoardDecision, BoardMeeting, Board, Agenda, ApplicationBatch
from .models import BoardMember, InterestDeclaration, MeetingAttendee, AgendaItem

fake = Faker()


agenda = Recipe(
    Agenda
)

agendaitem = Recipe(
    AgendaItem
)

applicationbatch = Recipe(
    ApplicationBatch
)

board = Recipe(
    Board,
)

boarddecision = Recipe(
    BoardDecision,
)

boardmeeting = Recipe(
    BoardMeeting,
)

boardmember = Recipe(
    BoardMember,
    board_join_date=dateutil.utils.today()
)

interestdeclaration = Recipe(
    InterestDeclaration,
)

meetingattendee = Recipe(
    MeetingAttendee,
)