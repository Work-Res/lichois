from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import ParentDetails
from ..forms import ParentDetailsForm


@admin.register(ParentDetails, site=citizenship_admin)
class ParentDetailsAdmin(admin.ModelAdmin):

    form = ParentDetailsForm
