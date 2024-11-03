import os

from unittest import mock
from django.test import TestCase
from django.contrib.auth.models import Group, Permission


from app.classes.permissions import GroupManager


class TestGroupManager(TestCase):

    def setUp(self):
        # Mocked file content for groups.txt
        self.group_file_content = """Group One:
    can_add_user
    can_change_user

Group Two:
    can_delete_user
"""
        # Mock the group file path
        self.group_file_path = '/path/to/groups.txt'

        # Mock `os.path.exists` to return True
        self.exists_patcher = mock.patch('os.path.exists', return_value=True)
        self.mock_exists = self.exists_patcher.start()

        # Prepare some permissions in the database
        Permission.objects.create(codename='can_add_user', name='Can add user', content_type_id=1)
        Permission.objects.create(codename='can_change_user', name='Can change user', content_type_id=1)
        Permission.objects.create(codename='can_delete_user', name='Can delete user', content_type_id=1)

    def tearDown(self):
        # Stop the patchers after each test
        self.exists_patcher.stop()

    @mock.patch('builtins.open', new_callable=mock.mock_open,
                read_data="Group One:\n    can_add_user\n    can_change_user\n\nGroup Two:\n    can_delete_user\n")
    def test_create_or_update_groups_creates_groups(self, mock_open):
        # Initialize the GroupManager with the mocked path

        manager = GroupManager(self.group_file_path)
        # Run the create or update groups method
        manager.create_or_update_groups()

        # Check if groups are created
        group_one = Group.objects.get(name="Group One")
        group_two = Group.objects.get(name="Group Two")

        self.assertIsNotNone(group_one)
        self.assertIsNotNone(group_two)

    def test_permissions_assigned_to_groups(self):
        # Initialize the GroupManager with the mocked path
        current_dir = os.path.dirname(__file__)
        group_file_path = os.path.join(current_dir, "data", "groups", "groups.txt")
        manager = GroupManager(group_file_path)

        # Run the create or update groups method
        manager.create_or_update_groups()

        groups = Group.objects.all()
        self.assertEqual(3, groups.count())

        # Check if permissions are assigned correctly to Group One
        group_one = Group.objects.get(name="Group One")
        self.assertTrue(group_one.permissions.filter(codename="can_update_app_initial").exists())
        self.assertTrue(group_one.permissions.filter(codename="can_delete_app_initial").exists())
        self.assertTrue(group_one.permissions.filter(codename="can_view_app_initial").exists())

        # Check if permissions are assigned correctly to Group Two
        group_two = Group.objects.get(name="Group Two")
        self.assertTrue(group_two.permissions.filter(codename="can_delete_app_verification").exists())
        self.assertTrue(group_two.permissions.filter(codename="can_view_app_production").exists())
        self.assertTrue(group_two.permissions.filter(codename="can_view_app_production").exists())

    @mock.patch('os.path.exists', return_value=False)
    def test_no_file_found(self, mock_exists):
        # Initialize the GroupManager with a path that does not exist
        manager = GroupManager(self.group_file_path)

        # Run the create or update groups method
        result = manager.create_or_update_groups()

        # Verify the output when the file does not exist
        self.assertIsNone(result)
