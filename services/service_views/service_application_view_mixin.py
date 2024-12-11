from app.api.dto import NewApplicationDTO
from app.classes import ApplicationService

from ..classes import ServicesApplicationFormsUrls
from app.utils import ApplicationStatusEnum


class ServiceApplicationViewMixin:

    def application_forms(
            self, model_cls_list=None,document_number=None, next_url=None):
        """Returns application forms and urls.
        """
    
        forms_urls = ServicesApplicationFormsUrls(
            document_number=document_number,
            non_citizen_identifier=self.non_citizen_identifier,
            application_models_cls=model_cls_list,
            next_url=next_url).application_urls()
        return forms_urls

    def application_number(self, process_name=None, application_type=None):
        """Returns an application number.
        """
        application_dto = NewApplicationDTO(
            process_name,
            self.non_citizen_identifier,
            status=ApplicationStatusEnum.NEW.value,
            applicant_type='employee',
            dob=self.request.user.dob,
            work_place='Gaborone',
            full_name=self.request.user)
        application_service = ApplicationService(new_application_dto=application_dto)
        application, _ = application_service.create_application()

        return application.application_document.document_number

    @property
    def non_citizen_identifier(self):
        """Returns the applicant's non_citizen_identifier.
        """
        return self.request.user.non_citizen_identifier

    @property
    def personal_details(self):
        """Returns personal details.
        """
        
        personal_details = {
            'Fullname': f'{self.request.user.first_name} {self.request.user.last_name}',
            'Email': self.request.user.email,
            'Date of Birth': self.request.user.dob,
            'Non Citizen Identifier': self.request.user.non_citizen_identifier}
        return personal_details
    