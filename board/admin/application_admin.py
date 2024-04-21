from django.contrib import admin
from ..admin_site import decision_admin
from ..models import Application
from ..forms import ApplicationForm


@admin.register(Application, site=decision_admin)
class ApplicationAdmin(admin.ModelAdmin):

    form = ApplicationForm
