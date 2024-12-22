from django.views.generic import TemplateView


from app.models import Application
from app.utils import ApplicationProcesses
from app_personal_details.models import Permit

from ..applicant_details_view_mixin import ApplicationDetailsViewMixin


class WorkResidentPermitDashboardView(TemplateView, ApplicationDetailsViewMixin):
    template_name = 'applications/work-res/work-res-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        next_url = 'work_res_permit_dashboard'
        context.update(
            new_application_required=self.new_application_required,
            next_url=next_url,

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
        #Get Moffat to impliment
        return False
