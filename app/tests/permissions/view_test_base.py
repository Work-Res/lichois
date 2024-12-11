
import os

from rest_framework.test import APITestCase
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.classes.permissions import GroupManager
from app.models import Application, ApplicationStatus
from app.utils import ApplicationProcesses, ApplicationStatusEnum, statuses
from authentication.models import User

from django.apps import apps
from app_checklist.apps import AppChecklistConfig


class ViewSetTestBase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_config = apps.get_app_config("app_checklist")
        if isinstance(app_config, AppChecklistConfig):
            app_config.ready()

    def create_application_statuses(self):
        for status in statuses:
            ApplicationStatus.objects.create(**status)

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            full_name="Test test",
            applicant_type="student"
        )

        self.application_service = ApplicationService(new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    def setUp(self):
        # Create test users
        self.create_application_statuses()
        self.application, self.version = self.create_new_application()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.other_user = User.objects.create_user(username="otheruser", password="password123")
        self.user_without_permission = User.objects.create_user(username="user_without_permission",
                                                                password="password123")

        content_type = ContentType.objects.get_for_model(Application)

        current_dir = os.path.dirname(__file__)
        group_file_path = os.path.join(current_dir, "data", "groups", "groups.txt")
        manager = GroupManager(group_file_path)

        # Run the create or update groups method
        manager.create_or_update_groups()

        self.group = Group.objects.get(name="App Group")

        # Create a group
        permissions = [
            ('can_update_app_initial', 'Can Update App Initial'),
            ('can_view_app_initial', 'Can View App Initial'),
            ('can_view_app_replacement', 'Can View App Replacement'),
            ('can_update_app_replacement', 'Can change App Replacement'),
            ('can_view_app_renewal', 'Can View App Renewal'),
            ('can_update_app_renewal', 'Can change App Renewal'),
            ('can_delete_app_initial', 'Can delete App')
        ]

        for codename, name in permissions:
            permission = Permission.objects.get(
                codename=codename,
                content_type=content_type
            )
            self.group.permissions.add(permission)

        # Add users to the group
        self.user.groups.add(self.group)
        self.other_user.groups.add(self.group)

        # Authenticate the test user
        self.client.force_authenticate(user=self.user)
