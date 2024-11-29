from django.contrib import admin
from ..models import Passport

class PassportAdmin(admin.ModelAdmin):
    list_display = ['passport_number', 'date_issued', 'place_issued', 'expiry_date', 'nationality', 'photo', 'previous_passport_number']
    search_fields = ['passport_number']