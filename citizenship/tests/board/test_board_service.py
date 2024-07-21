from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from citizenship.models.board import Member, Role
from citizenship.service.board import BoardService


class BoardServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.role1 = Role.objects.create(name='Role 1', description='Test role 1')
        self.role2 = Role.objects.create(name='Role 2', description='Test role 2')

    def test_create_board(self):
        board = BoardService.create_board(name='Board 1', description='Test board', quorum_roles=[
            self.role1, self.role2])
        self.assertIsNotNone(board.id)
        self.assertEqual(board.name, 'Board 1')
        self.assertEqual(board.description, 'Test board')
        self.assertEqual(board.quorum_roles.count(), 2)

    def test_update_board(self):
        board = BoardService.create_board(name='Board 1', description='Test board', quorum_roles=[self.role1])
        updated_board = BoardService.update_board(board_id=board.id, name='Updated Board',
                                                  description='Updated description', quorum_roles=[self.role1,
                                                                                                   self.role2])
        self.assertEqual(updated_board.name, 'Updated Board')
        self.assertEqual(updated_board.description, 'Updated description')
        self.assertEqual(updated_board.quorum_roles.count(), 2)

    def test_update_nonexistent_board(self):
        with self.assertRaises(ValidationError):
            BoardService.update_board(board_id=999, name='Updated Board', description='Updated description',
                                      quorum_roles=[self.role1, self.role2])

    def test_add_board_meeting_without_quorum(self):
        board = BoardService.create_board(name='Board 1', description='Test board', quorum_roles=[self.role1,
                                                                                                  self.role2])
        Member.objects.create(user=self.user, board=board, role=self.role1)  # Only one role satisfied
        with self.assertRaises(ValidationError):
            BoardService.add_board_meeting(
                board_id=board.id, title='Meeting 1', location='Conference Room',
                agenda='Discuss updates', status='Scheduled')

    def test_add_board_meeting_with_quorum(self):
        board = BoardService.create_board(
            name='Board 1', description='Test board', quorum_roles=[self.role1, self.role2])
        Member.objects.create(user=self.user,board=board, role=self.role1)
        Member.objects.create(user=User.objects.create_user(username='user2', password='pass'), board=board,
                              role=self.role2)
        meeting = BoardService.add_board_meeting(
            board_id=board.id, title='Meeting 1', location='Conference Room',
            agenda='Discuss updates', status='Scheduled')
        self.assertIsNotNone(meeting.id)
        self.assertEqual(meeting.title, 'Meeting 1')
        self.assertEqual(meeting.location, 'Conference Room')
        self.assertEqual(meeting.agenda, 'Discuss updates')
        self.assertEqual(meeting.status, 'Scheduled')
