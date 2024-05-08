from django.contrib import admin
from ..admin_site import board_admin
from ..models import BoardMember
from ..forms import BoardMemberForm


@admin.register(BoardMember, site=board_admin)
class BoardMemberAdmin(admin.ModelAdmin):

    form = BoardMemberForm
