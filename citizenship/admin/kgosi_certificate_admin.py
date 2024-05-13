from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import KgosiCertificate
from ..forms import KgosiCertificateForm


@admin.register(KgosiCertificate, site=citizenship_admin)
class KgosiCertificateAdmin(admin.ModelAdmin):

    form = KgosiCertificateForm
