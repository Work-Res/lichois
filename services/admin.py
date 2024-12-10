from django.contrib import admin

from .admin_site import services_admin
from .models import TestModel


@admin.register(TestModel, site=services_admin)
class TestModelAdmin(admin.ModelAdmin):
    pass
