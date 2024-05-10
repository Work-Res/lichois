from django.contrib import admin
from ..models import Agenda, AgendaItem
from ..forms import AgendaForm, AgendaItemForm


class AgendaAdmin(admin.ModelAdmin):
    form = AgendaForm


admin.site.register(Agenda, AgendaAdmin)
