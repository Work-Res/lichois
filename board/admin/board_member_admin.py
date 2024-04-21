from django.contrib import admin
from ..admin_site import decision_admin
from ..models import BoardMember
from ..forms import BoardMemberForm


@admin.register(BoardMember, site=decision_admin)
class BoardMemberAdmin(admin.ModelAdmin):

    form = BoardMemberForm
