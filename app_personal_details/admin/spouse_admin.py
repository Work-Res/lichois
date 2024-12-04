from django.contrib import admin
from ..models import Spouse

class SpouseAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'middle_name', 'maiden_name', 'country', 'place_birth', 'dob', 'passport']
    search_fields = ['first_name', 'last_name']
    

admin.site.register(Spouse, SpouseAdmin)