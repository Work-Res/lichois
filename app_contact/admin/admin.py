from django.contrib import admin
from ..models import (
    ApplicationContact
)
from .application_contact_admin import *

admin.site.register(ApplicationContact, ApplicationContactAdmin)
