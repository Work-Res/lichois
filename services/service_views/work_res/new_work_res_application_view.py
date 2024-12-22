from django.views.generic import TemplateView


from app.models import Application
from app.utils import ApplicationProcesses
from app_personal_details.models import Permit
from workresidentpermit.utils import WorkResidentPermitApplicationTypeEnum

from ...form_models import work_res_permit
from ..applicant_details_view_mixin import ApplicationDetailsViewMixin
from ..application_view_mixin import ApplicationViewMixin


class NewApplicationWorkResidentPermitDashboardView(
        TemplateView, ApplicationViewMixin, ApplicationDetailsViewMixin):
    template_name = 'applications/work-res/new_app_work_res_application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        next_url = 'new_app_work_res_permit_dashboard'

        context.update(
            application_forms=self.service_application_forms,
            next_url=next_url,
            non_citizen_identifier=self.non_citizen_identifier,
            personal_details=self.personal_details,
        )
        return context


    def create_or_get_appliation(self):
        """Returns an application.
        """
        try:
            application = Application.objects.get(
                process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
                application_document__applicant__user_identifier=self.non_citizen_identifier).exclude(
                    application_status__code__in=[
                        "COMPLETED", "CANCELLED", "REJECTED"])
        except Application.DoesNotExist:
            pass
        return application

    @property
    def service_application_forms(self, next_url=None):
        """Returns services forms with urls.
        """
        model_cls_list = work_res_permit  # This could come from a config file

        application_number = self.new_application_number(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            application_type=WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_ONLY.value)

        application_forms = self.application_forms(
            model_cls_list=model_cls_list,
            document_number=application_number,
            next_url=next_url)
        return application_forms

    @property
    def permits(self):
        """Returns a list of all work and res permits.
        """
        permits = Permit.objects.filter(
            permit_type=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            non_citizen_identifier=self.non_citizen_identifier)
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
    def new_application_required(self):
        """Return true if a new application is in progress.
        """
        if self.active_permit and self.active_application:
            return False
        return True

    @property
    def active_permit(self):
        """Return True if there is an active permit.
        """
        for permit in self.permits:
            if not permit.expired:
                return True
        return False

    def active_application(self):
        """Returns True of there is an active application in progress.
        """
        # Get Moffat to impliment
        return False

    @property
    def create_new_application(self):
        """Returns an application number for work and residence permit.
        """
        new_app = self.request.GET.get('new_application', False)
        if new_app:
            # Generate a new application number
            return '123456'
        return None
