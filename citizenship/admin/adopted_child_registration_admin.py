from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import AdoptedChildRegistration
from ..forms import AdoptedChildRegistrationForm


@admin.register(AdoptedChildRegistration, site=citizenship_admin)
class AdoptedChildRegistrationAdmin(admin.ModelAdmin):

    form = AdoptedChildRegistrationForm
