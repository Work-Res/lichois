from .base_view import BaseView
from app_personal_details.models import (
    Person, Passport, Education, ParentalDetails,
    NextOfKin, Spouse, Child)
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact

from app_personal_details.admin_site import personal_details_admin

class NewWorkResApplicationsView(BaseView):

    def get_specific_context(self):
        model_cls_list = [
            [Person, personal_details_admin.name]]  # This could come from a config file
        
        context = {}
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
            document_number=self.application_number(),
            new_application=self.new_application,
            create_new_application=self.create_new_application,
            application_forms=self.application_forms(
                model_cls_list=model_cls_list)
        )

