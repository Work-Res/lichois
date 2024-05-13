from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import CitizenSponsorCertificate
from ..forms import CitizenSponsorCertificateForm


@admin.register(CitizenSponsorCertificate, site=citizenship_admin)
class CitizenSponsorCertificateAdmin(admin.ModelAdmin):

    form = CitizenSponsorCertificateForm
