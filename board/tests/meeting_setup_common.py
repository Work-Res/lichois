import uuid
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy


class CommonSetupTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='password123')

        self.board = mommy.make_recipe(
            'board.board',
            id=uuid.uuid4()
        )

        self.board_member = mommy.make_recipe(
            'board.boardmember',
            id=uuid.uuid4(),
            board=self.board,
            user_id=1
        )

        self.board_member2 = mommy.make_recipe(
            'board.boardmember',
            id=uuid.uuid4(),
            board=self.board,
            user_id=2
        )

        self.board_member3 = mommy.make_recipe(
            'board.boardmember',
            id=uuid.uuid4(),
            board=self.board
        )

        self.board_meeting = mommy.make_recipe(
            'board.boardmeeting',
            id=uuid.uuid4(),
            board_id=self.board.id
        )

        self.agenda = mommy.make_recipe(
            'board.agenda',
            id=uuid.uuid4(),
            meeting=self.board_meeting
        )

        self.agenda_item1 = mommy.make_recipe(
            'board.agendaitem',
            id=uuid.uuid4()
        )

        self.agenda_item2 = mommy.make_recipe(
            'board.agendaitem',
            id=uuid.uuid4()
        )