from django.contrib import admin
from ..admin_site import board_admin
from ..models import VotingProcess
from ..forms import VotingProcessForm


class VotingProcessAdmin(admin.ModelAdmin):
	form = VotingProcessForm


board_admin.register(VotingProcess, VotingProcessAdmin)
