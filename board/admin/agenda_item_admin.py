from django.contrib import admin
from ..models import AgendaItem
from ..forms import AgendaItemForm
from ..admin_site import board_admin


class AgendaItemAdmin(admin.ModelAdmin):
	form = AgendaItemForm


board_admin.register(AgendaItem, AgendaItemAdmin)
