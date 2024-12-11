from django.views.generic import TemplateView


from app.models import Application
from app.utils import ApplicationProcesses
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum
from app_personal_details.models import Permit

from ...form_models import work_res_permit
from ..service_application_view_mixin import ServiceApplicationViewMixin


class WorkResidentPermitDashboardView(TemplateView, ServiceApplicationViewMixin):
    template_name = 'applications/work-res/work-res-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model_cls_list = work_res_permit  # This could come from a config file
        
        application_number = self.application_number(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            application_type= WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_ONLY.value)

        next_url = 'work_res_permit_dashboard'
        context.update(
            new_application=self.new_application,
            create_new_application=self.create_new_application,
            application_forms=self.application_forms(
                model_cls_list=model_cls_list,
                document_number=application_number,
                next_url=next_url),
            next_url=next_url,
            
            document_number=application_number,
            non_citizen_identifier=self.non_citizen_identifier,
            personal_details=self.personal_details,
            
            permits=self.permits
        )
        return context

    @property
    def permits(self):
        """Returns a list of all work and res permits.
        """
        permits = Permit.objects.filter(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            application_document__applicant__user_identifier=self.non_citizen_identifier)
        return permits

    @property
    def applications(self):
        """Returns a list of all applications.
        """
        applications = Application.objects.filter(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            application_document__applicant__user_identifier=self.non_citizen_identifier)
        return applications
    

    @property
    def new_application(self):
        """Return true if a new application is in progress.
        """
        if self.permits:
            return False
        return True

    @property
    def create_new_application(self):
        """Returns an application number for work and residence permit.
        """
        new_app = self.request.GET.get('new_application', False)
        if new_app:
            # Generate a new application number
            return '123456'
        return None
