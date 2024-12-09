from django.contrib import admin
from ..models import ParentalDetails


from ..admin_site import personal_details_admin


@admin.register(ParentalDetails, site=personal_details_admin)
class ParentalDetailsAdmin(admin.ModelAdmin):
    list_display = ['father', 'mother', 'father_address', 'mother_address']
    search_fields = ['father', 'mother']
