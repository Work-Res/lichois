from django.contrib import admin
from ..models import Application
from ..forms import ApplicationForm
from ..admin_site import app_admin


class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationForm


app_admin.register(Application, ApplicationAdmin)
