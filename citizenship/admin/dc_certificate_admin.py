from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import DCCertificate
from ..forms import DCCertificateForm


@admin.register(DCCertificate, site=citizenship_admin)
class DCCertificateAdmin(admin.ModelAdmin):

    form = DCCertificateForm
