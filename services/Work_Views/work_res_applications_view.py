from django.views.generic import TemplateView

from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact
from app_personal_details.models import (
    Person, Passport, Education, ParentalDetails,
    NextOfKin, Spouse, Child)
from workresidentpermit.models import ResidencePermit, WorkPermit

from .service_application_view_mixin import ServiceApplicationViewMixin


class WorkPermitDashboardView(TemplateView, ServiceApplicationViewMixin):
    template_name = 'applications/work-res/work-res-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model_cls_list = [
            Person, ApplicationAddress,
            ApplicationContact, Passport, Education,
            ParentalDetails, Spouse,
            Child]  # This could come from a config file

        context["permit_name"] = "Work & Residence Permit"
        context["total_applications"] = 3
        context["completed_applications"] = 2
        context["pending_applications"] = 0
        context["in_progress_applications"] = 1

        test_permit = dict(
            permit_number="WR1234",
            applicant_name="Peter Parker",
            permit_type="Work and Residence Permit",
            start_date="2024-01-04",
            expiry_date="2027-04-23",
            status='active'
        )

        context["permits"] = [test_permit]

        context.update(
            application_number=self.application_number(),
            new_application=self.new_application,
            create_new_application=self.create_new_application,
            application_forms=self.application_forms(
                model_cls_list=model_cls_list)
        )

        return context

    def permits(self):
        """Returns a list of all work and res permits.
        """
        return None

    @property
    def new_application(self):
        """Return true if a new application is in progress.
        """
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
