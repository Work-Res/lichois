from django.contrib import admin
from ..models import ApplicationStatus
from ..forms import ApplicationStatusForm
from ..admin_site import app_admin


class ApplicationStatusAdmin(admin.ModelAdmin):
    form = ApplicationStatusForm


app_admin.register(ApplicationStatus, ApplicationStatusAdmin)
