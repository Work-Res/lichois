from django.contrib import admin
from ..admin_site import decision_admin
from ..models import Board
from ..forms import BoardForm


@admin.register(Board, site=decision_admin)
class BoardAdmin(admin.ModelAdmin):

    form = BoardForm
