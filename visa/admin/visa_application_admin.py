from django.contrib import admin
from ..admin_site import visa_admin
from ..forms import VisaApplicationForm
from ..models import VisaApplication, VisaReferenceInline, DisposalMoneyInline
from ..models import ContactMethodInline


@admin.register(VisaReferenceInline, site=visa_admin)
class VisaReferenceInlineAdmin(admin.ModelAdmin):
    pass


class VisaReferenceInline(admin.StackedInline):
    model = VisaReferenceInline


@admin.register(DisposalMoneyInline, site=visa_admin)
class DisposalMoneyInlineAdmin(admin.ModelAdmin):
    pass


class DisposalMoneyInline(admin.StackedInline):
    model = DisposalMoneyInline


@admin.register(ContactMethodInline, site=visa_admin)
class ContactMethodInlineAdmin(admin.ModelAdmin):
    pass


class ContactMethodInline(admin.StackedInline):
    model = ContactMethodInline

@admin.register(VisaApplication, site=visa_admin)
class VisaApplicationAdmin(admin.ModelAdmin):

    form = VisaApplicationForm

    list_filter = ('country_birth', 'visa_type', 'no_of_entries')

    list_display = ('country_birth', 'visa_type', 'no_of_entries')

    inlines = [VisaReferenceInline, DisposalMoneyInline, ContactMethodInline]

    fieldsets = (
        (None, {
            'fields': ('first_name',
                       'last_name',
                       'middle_name',
                       'maiden_name',
                       # 'age', calculated field
                       'dob',
                       'country_birth',
                       'place_birth',
                       'gender',
                       'marital_status',
                       'nationality',
                       'visa_type',
                       'no_of_entries',
                       # bots_address,
                       # dom_address,
                       'occupation',
                       'qualifications',
                       'durations_stay',
                       'travel_reasons',
                       'requested_valid_from',
                       'requested_valid_to',
                       'return_visa_to',
                       'return_valid_until')},
         ),
        ('Audit Fields', {
            'fields': ('created',
                       'modified',
                       'user_created',
                       'user_modified',
                       'hostname_created',
                       'hostname_modified'),
            'classes': ('collapse',),
        }),
    )
    radio_fields = {'gender': admin.VERTICAL,
                    'marital_status': admin.VERTICAL,
                    'visa_type': admin.VERTICAL,
                    'no_of_entries': admin.VERTICAL}

