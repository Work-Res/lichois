from app.models import Application
from app.utils import ApplicationStatusEnum
from app_checklist.models import SystemParameter
from board.models import ApplicationBatch
from workflow.models import Task
from workresidentpermit.classes.service import DeferredApplicationService
from .base_test_setup import BaseTestSetup
from ..api.dto import RequestDeferredApplicationDTO
from ..classes import WorkResidentPermitApplication

from datetime import date


class TestDeferredApplicationService(BaseTestSetup):

    def test_validate(self):
        work_resident_permit_application = WorkResidentPermitApplication(
            document_number=self.document_number,
        )
        response = work_resident_permit_application.submit()
        message = "Application has been submitted successfully."
        status = message in [message.get("details") for message in response.messages]
        self.assertTrue(status)

        tasks_count = Task.objects.filter(activity__process__document_number=self.document_number).count()
        self.assertEqual(tasks_count, 1)
        app = Application.objects.get(application_document__document_number=self.document_number)

        self.assertEqual(app.application_status.code.upper(), ApplicationStatusEnum.VERIFICATION.value.upper())

        application_batch = ApplicationBatch.objects.create(
            batch_type="Batch_type"
        )
        application_batch.applications.add(app)
        application_batch.save()

        request_dto = RequestDeferredApplicationDTO(
            document_number=self.document_number,
            comment="Testing deferred application",
            deferred_from="Commisioner's Officer",
            expected_action="FURTHER_INVESTIGATION",
            # task_details_config_file = task_details_config_file
            batch_id=application_batch.id,
        )

        deferred_application_service = DeferredApplicationService(
            request_deferred_application_dto=request_dto
        )
        self.assertTrue(deferred_application_service.validate())

    def test_create_deferred_task(self):
        work_resident_permit_application = WorkResidentPermitApplication(
            document_number=self.document_number,
        )
        response = work_resident_permit_application.submit()
        message = "Application has been submitted successfully."
        status = message in [message.get("details") for message in response.messages]
        self.assertTrue(status)

        tasks_count = Task.objects.filter(activity__process__document_number=self.document_number).count()
        self.assertEqual(tasks_count, 1)
        app = Application.objects.get(application_document__document_number=self.document_number)

        self.assertEqual(app.application_status.code.upper(), ApplicationStatusEnum.VERIFICATION.value.upper())

        application_batch = ApplicationBatch.objects.create(
            batch_type="Batch_type"
        )
        application_batch.applications.add(app)
        application_batch.save()

        request_dto = RequestDeferredApplicationDTO(
            document_number=self.document_number,
            comment="Testing deferred application",
            deferred_from="Commisioner's Officer",
            expected_action="FURTHER_INVESTIGATION",
            # task_details_config_file = task_details_config_file
            batch_id=application_batch.id,
        )

        deferred_application_service = DeferredApplicationService(
            request_deferred_application_dto=request_dto
        )

        SystemParameter.objects.create(
            duration=1,
            application_type="DEFERRED_APPLICATION_DURATION",
            duration_type="days",
            valid_from=date.today(),
            valid_to=date(2024, 12, 12)
        )
        self.assertTrue(deferred_application_service.create_deferred_task())

    def test_remove_application_batch_and_update_application(self):
        work_resident_permit_application = WorkResidentPermitApplication(
            document_number=self.document_number,
        )
        response = work_resident_permit_application.submit()
        message = "Application has been submitted successfully."
        status = message in [message.get("details") for message in response.messages]
        self.assertTrue(status)

        tasks_count = Task.objects.filter(activity__process__document_number=self.document_number).count()
        self.assertEqual(tasks_count, 1)
        app = Application.objects.get(application_document__document_number=self.document_number)

        self.assertEqual(app.application_status.code.upper(), ApplicationStatusEnum.VERIFICATION.value.upper())

        application_batch = ApplicationBatch.objects.create(
            batch_type="Batch_type"
        )
        application_batch.applications.add(app)
        application_batch.save()

        request_dto = RequestDeferredApplicationDTO(
            document_number=self.document_number,
            comment="Testing deferred application",
            deferred_from="Commisioner's Officer",
            expected_action="FURTHER_INVESTIGATION",
            # task_details_config_file = task_details_config_file
            batch_id=application_batch.id,
        )

        deferred_application_service = DeferredApplicationService(
            request_deferred_application_dto=request_dto
        )

        SystemParameter.objects.create(
            duration=1,
            application_type="DEFERRED_APPLICATION_DURATION",
            duration_type="days",
            valid_from=date.today(),
            valid_to=date(2024, 12, 12)
        )
        self.assertTrue(deferred_application_service.remove_application_batch())
        self.assertTrue(deferred_application_service.update_application())

    def test_create_deferred_application(self):
        work_resident_permit_application = WorkResidentPermitApplication(
            document_number=self.document_number,
        )
        response = work_resident_permit_application.submit()
        message = "Application has been submitted successfully."
        status = message in [message.get("details") for message in response.messages]
        self.assertTrue(status)

        tasks_count = Task.objects.filter(activity__process__document_number=self.document_number).count()
        self.assertEqual(tasks_count, 1)
        app = Application.objects.get(application_document__document_number=self.document_number)

        self.assertEqual(app.application_status.code.upper(), ApplicationStatusEnum.VERIFICATION.value.upper())

        application_batch = ApplicationBatch.objects.create(
            batch_type="Batch_type"
        )
        application_batch.applications.add(app)
        application_batch.save()

        request_dto = RequestDeferredApplicationDTO(
            document_number=self.document_number,
            comment="Testing deferred application",
            deferred_from="Commisioner's Officer",
            expected_action="FURTHER_INVESTIGATION",
            # task_details_config_file = task_details_config_file
            batch_id=application_batch.id,
        )

        deferred_application_service = DeferredApplicationService(
            request_deferred_application_dto=request_dto
        )

        SystemParameter.objects.create(
            duration=1,
            application_type="DEFERRED_APPLICATION_DURATION",
            duration_type="days",
            valid_from=date.today(),
            valid_to=date(2024, 12, 12)
        )
        self.assertTrue(deferred_application_service.create())
