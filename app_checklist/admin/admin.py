from django.contrib import admin
from app_checklist.models import ChecklistClassifierItem, ChecklistClassifier, ClassifierItem, OfficeLocationClassifierItem, OfficeLocationClassifier

#Admin class for ChecklistClassifierItem
class ChecklistClassifierItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'application_type', 'mandatory', 'checklist_classifier', 'sequence', 'valid_from', 'valid_to')
    search_fields = ('code', 'name', 'application_type', 'description')
    list_filter = ('mandatory', 'valid_from', 'valid_to', 'checklist_classifier')
    ordering = ('sequence', 'valid_from')

#Admin class for ChecklistClassifier
class ChecklistClassifierAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'process_name', 'valid_from', 'valid_to')
    search_fields = ('code', 'name', 'process_name', 'description')
    list_filter = ('valid_from', 'valid_to')
    ordering = ('-created')

#Admin class for ClassifierItem
class ClassifierItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'process', 'mandatory', 'classifier', 'sequence', 'valid_from', 'valid_to')
    search_fields = ('code', 'name', 'process', 'description')
    list_filter = ('mandatory', 'valid_from', 'valid_to', 'classifier')
    ordering = ('sequence', 'valid_from')

#Admin class for OfficeLocationClassifier
class OfficeLocationClassifierItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'office_location_classifier', 'valid_from', 'valid_to')
    search_fields = ('code', 'name', 'description')
    list_filter = ('office_location_classifier', 'valid_from', 'valid_to')
    ordering = ('-created')

#Admin class for OfficeLocationClassifier
class OfficeLocationClassifierAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'valid_from', 'valid_to')
    search_fields = ('code', 'name', 'description')
    list_filter = ('valid_from', 'valid_to')
    ordering = ('-created')

# Register the models with their respective custom admin classes
admin.site.register(ChecklistClassifierItem, ChecklistClassifierItemAdmin)
admin.site.register(ChecklistClassifier, ChecklistClassifierAdmin)
admin.site.register(ClassifierItem, ClassifierItemAdmin)
admin.site.register(OfficeLocationClassifierItem, OfficeLocationClassifierItemAdmin)
admin.site.register(OfficeLocationClassifier, OfficeLocationClassifierAdmin)
