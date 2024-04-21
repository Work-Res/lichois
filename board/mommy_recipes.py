import uuid
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import BoardDecision, BoardMeeting, Application, Board, Agenda
from .models import BoardMember, InterestDeclaration, MeetingAttendee, AgendaItem

fake = Faker()

application = Recipe(
    Application,
)

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
    id=uuid.uuid4()
)

interestdeclaration = Recipe(
    InterestDeclaration,
)

meetingattendee = Recipe(
    MeetingAttendee,
    board_id=uuid.uuid4()
)