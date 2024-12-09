from django.contrib import admin
from ..models import Child

from ..admin_site import personal_details_admin


@admin.register(Child, site=personal_details_admin)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'dob', 'age', 'gender']
    search_fields = ['first_name', 'last_name']

