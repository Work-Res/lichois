import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from app_checklist.models import Region
from citizenship.models import Board, Role
from citizenship.service.board import BoardService


class BoardServiceTestCase(TestCase):

    def setUp(self):
        # Create Region
        self.region = Region.objects.create(
            name='Test Region',
            code='TR01',
            description='A test region',
            valid_from=timezone.now().date(),
            valid_to=(timezone.now() + timezone.timedelta(days=365)).date(),
            active=True
        )

        # Create Roles
        self.role1 = Role.objects.create(name='Role 1', description='First role')
        self.role2 = Role.objects.create(name='Role 2', description='Second role')

        # Create Board
        self.board = Board.objects.create(
            name='Test Board',
            region=self.region,
            description='A test board'
        )
        self.board.quorum_roles.set([self.role1, self.role2])
        self.board.save()

    def test_create_board(self):
        board = BoardService.create_board(
            name='New Board',
            region_id=self.region.id,
            description='A new test board',
            quorum_role_ids=[self.role1.id, self.role2.id]
        )
        self.assertIsNotNone(board)
        self.assertEqual(board.name, 'New Board')
        self.assertEqual(board.region, self.region)
        self.assertEqual(board.description, 'A new test board')
        self.assertTrue(board.quorum_roles.filter(id=self.role1.id).exists())
        self.assertTrue(board.quorum_roles.filter(id=self.role2.id).exists())

    def test_create_board_with_invalid_region(self):
        with self.assertRaises(ValidationError):
            BoardService.create_board(
                name='New Board',
                region_id=999,
                description='A new test board',
                quorum_role_ids=[self.role1.id, self.role2.id]
            )

    def test_get_board(self):
        board = BoardService.get_board(self.board.id)
        self.assertIsNotNone(board)
        self.assertEqual(board.name, 'Test Board')

    def test_get_board_invalid(self):
        with self.assertRaises(ValidationError):
            BoardService.get_board(999)

    def test_update_board(self):
        updated_board = BoardService.update_board(
            board_id=self.board.id,
            name='Updated Board',
            region_id=self.region.id,
            description='An updated test board',
            quorum_role_ids=[self.role1.id]
        )
        self.assertEqual(updated_board.name, 'Updated Board')
        self.assertEqual(updated_board.description, 'An updated test board')
        self.assertTrue(updated_board.quorum_roles.filter(id=self.role1.id).exists())
        self.assertFalse(updated_board.quorum_roles.filter(id=self.role2.id).exists())

    def test_update_board_invalid(self):
        with self.assertRaises(ValidationError):
            BoardService.update_board(
                board_id=999,
                name='Updated Board',
                region_id=self.region.id,
                description='An updated test board',
                quorum_role_ids=[self.role1.id]
            )

    def test_delete_board(self):
        result = BoardService.delete_board(self.board.id)
        self.assertTrue(result)
        with self.assertRaises(ValidationError):
            BoardService.get_board(self.board.id)

    def test_delete_board_invalid(self):
        with self.assertRaises(ValidationError):
            BoardService.delete_board(999)
