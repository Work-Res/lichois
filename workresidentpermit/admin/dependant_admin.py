from django.contrib import admin
from typing import Tuple
from ..models import Dependant


class DependantAdmin(admin.ModelAdmin):
    list_display: Tuple[str, ...] = (
        'name',
        'age',
        'gender',
    )
    search_fields: Tuple[str, ...] = ('name', 'gender')
    list_filter: Tuple[str, ...] = ('gender', 'age')

admin.site.register(Dependant, DependantAdmin)