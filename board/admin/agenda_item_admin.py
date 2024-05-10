from django.contrib import admin
from ..models import Agenda, AgendaItem
from ..forms import AgendaForm, AgendaItemForm


class AgendaItemAdmin(admin.ModelAdmin):
    form = AgendaItemForm


admin.site.register(AgendaItem, AgendaItemAdmin)
