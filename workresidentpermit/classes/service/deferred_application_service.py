from workresidentpermit.api.dto import RequestDeferredApplicationDTO


class DeferredApplicationService(CreateTask):

    def __init__(self, request_deferred_application_dto: RequestDeferredApplicationDTO):
        self.request_deferred_application_dto = request_deferred_application_dto

    def create_deferred_task(self):
        return self.new_task()

    def update_application(self):
        pass


    def dddd(self):
        pass
