from django.contrib import admin

from ..models import Dependant


class DependantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'age',
        'gender',
    )
    search_fields = ('name', 'gender')
    list_filter = ('gender', 'age')

admin.site.register(Dependant, DependantAdmin)