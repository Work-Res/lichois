from django.contrib import admin
from ..models import Child

class ChildAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'dob', 'age', 'gender']
    search_fields = ['first_name', 'last_name']

admin.site.register(Child, ChildAdmin)
