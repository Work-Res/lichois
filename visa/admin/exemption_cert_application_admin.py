from django.contrib import admin
from ..admin_site import visa_admin
from ..models import ExemptionCertificateApplication
from ..models import ExemptionCertificateDependantsInline
from ..forms import ExemptionCertificateApplicationForm


@admin.register(ExemptionCertificateDependantsInline, site=visa_admin)
class ExemptionCertificateDependantsInlineAdmin(admin.ModelAdmin):
    pass


class ExemptionCertificateDependantsInline(admin.StackedInline):
    model = ExemptionCertificateDependantsInline


@admin.register(ExemptionCertificateApplication, site=visa_admin)
class ExemptionCertificateApplicationAdmin(admin.ModelAdmin):

    form = ExemptionCertificateApplicationForm

    # list_filter = ()

    # list_display = ()

    inlines = [ExemptionCertificateDependantsInline, ]

    fieldsets = (
        (None, {
            'fields': ('last_name',
                       'first_name',
                       'middle_name',
                       'maiden_name',
                       'marital_status',
                       # 'age', calculated field
                       'dob',
                       'gender',
                       'country_birth',
                       'place_birth',
                       'pass_no',
                       'place_issued',
                       'date_issued',
                       'expiry_date',
                       'nationality',
                       'business_name',
                       # address,
                       'employment_capacity',
                       'qualification_experience',
                       'engagement_period',
                       'engagement_period_measure',
                       'declaration_fname',
                       'declaration_lname',
                       'declaration_date',
                       'signature',
                       'declaration_place',
                       'oath_datetime',
                       'commissioner_name',
                       'commissioner_designation',
                       'telephone_number',
                       'commissioner_signature')},
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
                    'marital_status': admin.VERTICAL}

