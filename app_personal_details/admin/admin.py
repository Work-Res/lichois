from django.contrib import admin
from ..models import (
    Person,
    Spouse,
    Passport,
    ParentalDetails,
    Education,
    Child
)

from .person_admin import *
from .spouse_admin import *
from .passport_admin import *
from .parental_details_admin import *
from .education_admin import *
from .child_admin import *

admin.site.register(Person, PersonAdmin)
admin.site.register(Spouse, SpouseAdmin)
admin.site.register(Passport, PassportAdmin)
admin.site.register(ParentalDetails, ParentalDetailsAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Child, ChildAdmin)