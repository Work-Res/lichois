from django.contrib import admin
from ..models import Agenda
from ..forms import AgendaForm
from ..admin_site import board_admin


class AgendaAdmin(admin.ModelAdmin):
    form = AgendaForm


board_admin.register(Agenda, AgendaAdmin)
