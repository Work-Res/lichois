from django.contrib import admin
from ..models import Education


from ..admin_site import personal_details_admin


@admin.register(Education, site=personal_details_admin)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['level', 'field_of_study', 'institution', 'start_date', 'end_date']
    search_fields = ['field_of_study', 'institution']
