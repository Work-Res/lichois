import logging

from app.api.common.web import APIResponse, APIMessage
from app.models import Application, ApplicationStatus, DeferredApplication
from app.utils import ApplicationStatusEnum
from board.models import ApplicationBatch
from workresidentpermit.api.dto import RequestDeferredApplicationDTO
from .create_task_service import CreateTaskService


class DeferredApplicationService(CreateTaskService):

    def __init__(self, request_deferred_application_dto: RequestDeferredApplicationDTO):
        self.request_deferred_application_dto = request_deferred_application_dto
        self.logger = logging.getLogger(__name__)
        self.response = APIResponse()
        super().__init__(request_dto=request_deferred_application_dto)

    def validate(self):
        """ Check if the deferred request exists before creating new one."""
        try:
            Application.objects.get(
                application_document__document_number=self.request_deferred_application_dto.document_number,
                application_status__code__iexact=ApplicationStatusEnum.DEFERRED.value
            )
        except Application.DoesNotExist:
            return True
        else:
            self.logger.info("Deferred Application: already exists.")
            api_message = APIMessage(
                code=400,
                message=f"Deferred Application  already exists.",
                details=f"Deferred Applicaiton with {self.request_deferred_application_dto.document_number} "
                        f"already exists."
            )
            self.response.messages.append(api_message.to_dict())
            return False

    def create_deferred_application(self):
        DeferredApplication.objects.create(
            application=self.application(),
            comment=self.request_deferred_application_dto.comment,
            deferred_from=self.request_deferred_application_dto.deferred_from,
            expected_action=self.request_deferred_application_dto.expected_action,
            deferred_status=self.application_status(ApplicationStatusEnum.PENDING.value)
        )

    def remove_application_batch(self):
        try:
            application_batch = ApplicationBatch.objects.get(id=self.request_deferred_application_dto.batch_id)
            application_batch.applications.remove(self.application())
            application_batch.save()
        except ApplicationBatch.DoesNotExist:
            api_message = APIMessage(
                code=400,
                message=f"ApplicationBatch  does not exists.",
                details=f"An application batch with {self.request_deferred_application_dto.batch_id} "
                        f"does not exists."
            )
            self.response.messages.append(api_message.to_dict())
        else:
            return True

    def application_status(self, status):
        return ApplicationStatus.objects.get(code__iexact=status)

    def application(self):
        return Application.objects.get(
            application_document__document_number=self.request_deferred_application_dto.document_number)

    def create_deferred_task(self):
        self.logger.info("Deferred Application: START creating a task.")
        return self.create_task()

    def update_application(self):
        try:
            self.logger.info("Deferred Application: START Updating.")
            application = self.application()
            application.application_status = self.application_status(ApplicationStatusEnum.DEFERRED.value)
            application.batched = False
            application.save()
            return application
        except Application.DoesNotExist as ex:
            self.logger.error(f"An error occurred, {ex}")
            api_message = APIMessage(
                code=400,
                message=f"Application  does not exists.",
                details=f"An applicaiton with {self.request_deferred_application_dto.document_number} "
                        f"does not exists."
            )
            self.response.messages.append(api_message.to_dict())
        except ApplicationStatus.DoesNotExist as ex:
            self.logger.error(f"An error occurred, {ex}")
            api_message = APIMessage(
                code=400,
                message=f"Application Status for deferred does not exists .",
                details=f"An application with status {ApplicationStatusEnum.DEFERRED.value} "
                        f"does not exists. Please report to developers."
            )
            self.response.messages.append(api_message.to_dict())
        else:
            self.logger.info("Deferred Application: END Updating.")
            return True

    def create(self):
        if self.validate():
            self.logger.info("Deferred Application: Validated successfully.")
            self.create_deferred_task()
            self.update_application()
            self.create_deferred_application()
            self.remove_application_batch()
            self.logger.info("Deferred Application: created successfully.")
            return True
        else:
            return False

    def complete_deferred_application(self):
        application = self.application()
        application.application_status = self.application_status(ApplicationStatusEnum.VETTING.value)
        application.save()
