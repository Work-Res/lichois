from django.contrib import admin
from typing import Tuple
from ..models import Dependant
from ..forms.dependant_form import DependantForm


class DependantAdmin(admin.ModelAdmin):

    form = DependantForm
    list_display: Tuple[str, ...] = (
        'name',
        'age',
        'gender',
    )
    search_fields: Tuple[str, ...] = ('name', 'gender')
    list_filter: Tuple[str, ...] = ('gender', 'age')

admin.site.register(Dependant, DependantAdmin)