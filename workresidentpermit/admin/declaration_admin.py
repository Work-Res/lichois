from django.contrib import admin

from ..models import Declaration

class DeclarationAdmin(admin.ModelAdmin):
    list_display = (
        'declaration_fname',
        'declaration_lname',
        'declaration_date',
        'signature',
    )
    search_fields = ('declaration_fname', 'declaration_lname', 'signature',)
    list_filter = ('declaration_date',)

admin.site.register(Declaration, DeclarationAdmin)