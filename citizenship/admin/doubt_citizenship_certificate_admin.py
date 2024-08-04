from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import DoubtCitizenshipCertificate
from ..forms import DoubtCitizenshipCertificateForm


@admin.register(DoubtCitizenshipCertificate, site=citizenship_admin)
class DoubtCitizenshipCertificateAdmin(admin.ModelAdmin):
    # TODO: Implement fields

    form = DoubtCitizenshipCertificateForm
