from django.contrib import admin
from ..admin_site import visa_admin
from ..models import BlueCardApplication
from ..forms import BlueCardApplicationForm


@admin.register(BlueCardApplication, site=visa_admin)
class BlueCardApplicationAdmin(admin.ModelAdmin):

    form = BlueCardApplicationForm

    fieldsets = (
        ('Personal Fields', {
            'fields': ('first_name',
                       'last_name',
                       'middle_name',
                       'maiden_name',
                       'prev_bw_id',
                       # 'age', calculated field
                       'dob',
                       'place_birth',
                       'country_birth',)
        }),
        ('Current Nationality Details', {
            'fields': ('pass_no',
                       'date_issued',
                       'expiry_date',
                       'place_issued',
                       'present_nationality',)
        }),
        ('Contacts Information', {
            'fields': (# contacts, # residential address
            )
        }),
        (None, {
            'fields': ('occupation',
                       'qualification'
            )
        }),
        ('Details of Next of Kin', {
            'fields': ('nok_surname',
                       'nok_firstname',
                       'nok_cell_phone',
                       'nok_telephone',
                       'nok_relations')
        }),
        ('Declaration', {
            'fields': ('declaration_date',
                       'signature'
            ),
            'description': ('I hereby declare that the information provided by me in this application '
                            'is true, correct and complete to the best of my knowledge. I understand that '
                            'any incorrect, misleading or untrue information or withholding of any relevant '
                            'formation may affect the issuance of the Botswana Blue Card or shall result in '
                            'the revocation of the Blue Card.')

        }),
        ('Comissioner of Oath', {
            'fields': ('declaration_place',
                       'oath_datetime',
                       'commissioner_name',
                       'commissioner_designation',
                       'telephone_number',
                       'commissioner_signature')
        }),
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
