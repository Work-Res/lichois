from django.contrib import admin
from ..models import (
    Country, ApplicationAddress
)

from .country_admin import *
from .application_address_admin import *


admin.site.register(Country, CountryAdmin)
admin.site.register(ApplicationAddress, ApplicationAddressAdmin)
