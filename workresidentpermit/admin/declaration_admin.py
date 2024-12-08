from django.contrib import admin
from typing import Tuple
from ..models import Declaration

class DeclarationAdmin(admin.ModelAdmin):
    list_display: Tuple[str, ...] = (
        'declaration_fname',
        'declaration_lname',
        'declaration_date',
        'signature',
    )
    search_fields: Tuple[str, ...] = ('declaration_fname', 'declaration_lname', 'signature',)
    list_filter: Tuple[str, ...] = ('declaration_date',)

admin.site.register(Declaration, DeclarationAdmin)