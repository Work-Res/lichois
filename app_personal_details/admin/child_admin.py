from django.contrib import admin
from ..models import Child

class ChildAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'dob', 'age', 'gender', 'is_applying_residence', 'is_adult', 'is_child']
    search_fields = ['first_name', 'last_name']