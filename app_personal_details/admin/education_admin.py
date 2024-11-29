from django.contrib import admin
from ..models import Education

class EducationAdmin(admin.ModelAdmin):
    list_display = ['level', 'field_of_study', 'institution', 'start_date', 'end_date']
    search_fields = ['field_of_study', 'institution']