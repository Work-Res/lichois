from django.contrib import admin
from ..models import Application
from ..forms import ApplicationForm
from ..admin_site import app_admin


class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationForm
    search_fields = ['application_document__document_number', 'process_name', 'application_type']


app_admin.register(Application, ApplicationAdmin)
