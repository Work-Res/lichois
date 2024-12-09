from django.contrib import admin

from ..models import Activity
from ..admin_site import workflow_admin


@admin.register(Activity, site=workflow_admin)
class ActivityAdmin(admin.ModelAdmin):
	list_display = ('name', 'process', 'sequence', 'valid_from', 'valid_to')
	search_fields = ('name', 'process__name')
	list_filter = ('process', 'valid_from', 'valid_to')
	ordering = ('sequence', 'valid_from')
	fields = (
	'process', 'name', 'description', 'sequence', 'create_task_rules', 'next_activity_name', 'valid_from', 'valid_to')

