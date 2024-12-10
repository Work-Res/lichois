from django.views.generic import TemplateView

from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact
from app_personal_details.models import (
    Person, Passport, Education, ParentalDetails,
    NextOfKin, Spouse, Child)

from .service_application_view_mixin import ServiceApplicationViewMixin


class ProfileView(TemplateView, ServiceApplicationViewMixin):
    template_name = 'two_factor/profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model_cls_list = [
            Person, ApplicationAddress,
            ApplicationContact, Passport, Education,
            ParentalDetails, Spouse, # NextOfKin, # FIX: The next of kin model causes the admin url generator class to throw an error when it tries to generate a link. 
            Child]  # This could come from a config file

        context.update(
            application_forms=self.application_forms(
                model_cls_list=model_cls_list),
            
            document_number=self.application_number(),
            non_citizen_identifier=self.non_citizen_identifier,
            personal_details=self.personal_details
        )
        return context
