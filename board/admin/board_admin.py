from django.contrib import admin
from ..admin_site import board_admin
from ..models import Board
from ..forms import BoardForm


@admin.register(Board, site=board_admin)
class BoardAdmin(admin.ModelAdmin):

    form = BoardForm
