from django.contrib import admin
from ..models import ApplicationBatch
from ..forms import ApplicationBatchForm
from ..admin_site import board_admin


class ApplicationBatchAdmin(admin.ModelAdmin):
	form = ApplicationBatchForm


board_admin.register(ApplicationBatch, ApplicationBatchAdmin)
