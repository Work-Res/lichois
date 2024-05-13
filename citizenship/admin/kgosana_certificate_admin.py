from django.contrib import admin
from ..admin_site import citizenship_admin
from ..models import KgosanaCertificate
from ..forms import KgosanaCertificateForm


@admin.register(KgosanaCertificate, site=citizenship_admin)
class KgosanaCertificateAdmin(admin.ModelAdmin):

    form = KgosanaCertificateForm
