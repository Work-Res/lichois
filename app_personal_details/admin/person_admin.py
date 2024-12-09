from django.contrib import admin
from ..models import Person


from ..admin_site import personal_details_admin


@admin.register(Person, site=personal_details_admin)
class PersonAdmin(admin.ModelAdmin):
    
    enable_nav_sidebar = False
    site_header = "MLHA Services Forms"
    site_title = "Customer Portal"
    index_title = "Welcome to MLHA Services"
    
    list_display = ['first_name', 'last_name', 'middle_name', 'maiden_name', 'marital_status', 'dob', 'gender', 'occupation', 'qualification', 'person_type', 'deceased']
    search_fields = ['first_name', 'last_name']
    fieldsets = (
        (None, {
            "fields": (
                'last_name', 'first_name',
                'middle_name', 'maiden_name',
                'marital_status', 'dob', 'gender',
                'occupation', 'qualification', 'person_type',
                'deceased'
            ),
        }),
    )
