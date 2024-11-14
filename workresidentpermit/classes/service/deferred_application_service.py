import logging

from app.api.common.web import APIResponse, APIMessage
from app.models import Application, ApplicationStatus, DeferredApplication
from app.utils import ApplicationStatusEnum
from app.workflow import ProductionTransactionData
from board.models import ApplicationBatch
from board.services import WorkflowManager
from workresidentpermit.api.dto import RequestDeferredApplicationDTO
from .create_task_service import CreateTaskService


class DeferredApplicationService(CreateTaskService):

    def __init__(self, request_deferred_application_dto: RequestDeferredApplicationDTO):
        self.request_deferred_application_dto = request_deferred_application_dto
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.response = APIResponse()
        super().__init__(request_dto=request_deferred_application_dto)

    def validate(self):
        """Check if the deferred request exists before creating new one."""
        try:
            Application.objects.get(
                application_document__document_number=self.request_deferred_application_dto.document_number,
                application_status__code__iexact=ApplicationStatusEnum.DEFERRED.value,
            )
        except Application.DoesNotExist:
            return True
        else:
            self.logger.info("Deferred Application: already exists.")
            api_message = APIMessage(
                code=400,
                message="Deferred Application  already exists.",
                details=f"Deferred Applicaiton with {self.request_deferred_application_dto.document_number} "
                        "already exists.",
            )
            self.response.messages.append(api_message.to_dict())
            return False

    def create_deferred_application(self):
        application = self.application()
        DeferredApplication.objects.create(
            previous_application_status=application.application_status,
            application=self.application(),
            comment=self.request_deferred_application_dto.comment,
            deferred_from=self.request_deferred_application_dto.deferred_from,
            expected_action=self.request_deferred_application_dto.expected_action,
            deferred_status=self.application_status(
                ApplicationStatusEnum.PENDING.value
            ),
        )

    def get_deferred_application(self):
        try:
            return DeferredApplication.objects.get(
                application__application_document__document_number=self.request_deferred_application_dto.document_number
            )
        except DeferredApplication.DoesNotExists:
            pass

    def remove_application_batch(self):
        try:
            application_batch = ApplicationBatch.objects.get(
                id=self.request_deferred_application_dto.batch_id
            )
            application_batch.applications.remove(self.application())
            application_batch.save()
        except ApplicationBatch.DoesNotExist:
            api_message = APIMessage(
                code=400,
                message=f"ApplicationBatch  does not exists.",
                details=f"An application batch with {self.request_deferred_application_dto.batch_id} "
                        f"does not exists.",
            )
            self.response.messages.append(api_message.to_dict())
        else:
            return True

    def application_status(self, status):
        return ApplicationStatus.objects.get(code__iexact=status)

    def application(self):
        return Application.objects.get(
            application_document__document_number=self.request_deferred_application_dto.document_number
        )

    def create_deferred_task(self):
        workflow = ProductionTransactionData()
        manager = WorkflowManager(
            workflow=workflow,
            application=self.application()
        )
        self.logger.info("Deferred Application: START creating a task.")
        manager.activate_next_task()

    def update_application(self):
        try:
            self.logger.info("Deferred Application: START Updating.")
            application = self.application()
            application.application_status = self.application_status(
                ApplicationStatusEnum.DEFERRED.value
            )
            application.batched = False
            application.save()
            return application
        except Application.DoesNotExist as ex:
            self.logger.error(f"An error occurred, {ex}")
            api_message = APIMessage(
                code=400,
                message=f"Application  does not exists.",
                details=f"An application with {self.request_deferred_application_dto.document_number} "
                        f"does not exists.",
            )
            self.response.messages.append(api_message.to_dict())
        except ApplicationStatus.DoesNotExist as ex:
            self.logger.error(f"An error occurred, {ex}")
            api_message = APIMessage(
                code=400,
                message="Application Status for deferred does not exists .",
                details=f"An application with status {ApplicationStatusEnum.DEFERRED.value} "
                        f"does not exists. Please report to developers.",
            )
            self.response.messages.append(api_message.to_dict())

    def create(self):
        self.logger.info("Starting the creation of Deferred Application.")

        if self.validate():
            self.logger.info("Deferred Application: Validation successful.")

            try:
                self.logger.info("Creating deferred application...")
                self.create_deferred_application()
                self.logger.info("Deferred application created successfully.")

                self.logger.info("Updating application...")
                self.update_application()
                self.logger.info("Application updated successfully.")

                self.logger.info("Creating deferred task...")
                self.create_deferred_task()
                self.logger.info("Deferred task created successfully.")

                self.logger.info("Removing application batch...")
                self.remove_application_batch()
                self.logger.info("Application batch removed successfully.")

                self.logger.info("Deferred Application: Creation process completed successfully.")
                return True

            except Exception as e:
                self.logger.error("Deferred Application: An error occurred during creation - %s", e, exc_info=True)
                return False
        else:
            self.logger.warning("Deferred Application: Validation failed.")
            return False

    def complete_deferred_application(self):
        deferred_application = self.get_deferred_application()
        application = self.application()
        application.application_status = deferred_application.previous_application_status
        application.save()
        deferred_application.deferred_status = self.application_status(status="ACCEPTED")
        deferred_application.save()
