from django.views.generic import TemplateView

from app.utils import ApplicationProcesses
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum
from workresidentpermit.models import WorkPermit, ResidencePermit

from services.form_models import replacement
from ..service_application_view_mixin import ServiceApplicationViewMixin


class WorkResidentPermitReplacementView(TemplateView, ServiceApplicationViewMixin):
    template_name = 'applications/work-res/work-res-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model_cls_list = replacement  # This could come from a config file

        context.update(
            new_application=self.new_application,
            create_new_application=self.create_new_application,
            application_forms=self.application_forms(
                model_cls_list=model_cls_list),
            
            document_number=self.generate_new_application_number,
            non_citizen_identifier=self.non_citizen_identifier,
            personal_details=self.personal_details,
            
            work_permits=self.work_permits,
            residence_permits=self.residence_permits
        )

        return context
    
    @property
    def generate_new_application_number(self):
        """Return a new application number.
        """
        application_number = self.new_application_number(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            application_type=WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_ONLY.value)
        return application_number

    @property
    def work_permits(self):
        """Returns a list of all work and res permits.
        """
        work_permits = WorkPermit.objects.filter(
            non_citizen_identifier=self.non_citizen_identifier)
        return work_permits

    @property
    def residence_permits(self):
        """Returns a list of all work and res permits.
        """
        residence_permits = ResidencePermit.objects.filter(
            non_citizen_identifier=self.non_citizen_identifier)
        return residence_permits

    @property
    def new_application(self):
        """Return true if a new application is in progress.
        """
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
