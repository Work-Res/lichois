from django.contrib import admin
from ..models import ParentalDetails

class ParentalDetailsAdmin(admin.ModelAdmin):
    list_display = ['father', 'mother', 'father_address', 'mother_address']
    search_fields = ['father', 'mother']