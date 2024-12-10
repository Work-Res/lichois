from django.contrib import admin

from ..admin_site import board_admin
from ..models import VotingProcess
from ..forms import VotingProcessForm


@admin.register(VotingProcess, site=board_admin)
class VotingProcessAdmin(admin.ModelAdmin):
	form = VotingProcessForm

