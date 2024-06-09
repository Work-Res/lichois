from django.db import models

from django.db.models.fields.json import JSONField

from app_comments.models import Comment
from . import ApplicationUser

from base_module.model_mixins import BaseUuidModel


class ApplicationRenewalHistory(BaseUuidModel):
    application_type = models.CharField(max_length=200)  # E.g WORK_PERMIT_EMERGECY
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    application_user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)  # user_identifier
    process_name = models.CharField(max_length=200)  # WORK_RESIDENT_PERMIT
    historical_record = JSONField()  # permit type , can be of anny type o

    def __str__(self):
        return f'{self.application_type} {self.process_name} {self.application_user.user_identifier}'

    class Meta:
        app_label = 'app'

# Test Case Scenario
# app1 - permit1
#  HistoryObject {
#     modified_date=when
#     data: [List of permits]
# }


# app2 - submit a renewal - register -> create ApplicationRenewalHistory(application_type=EMERGEY, commet="AAA",application_user="X", process_name="C", historical_record={
# permits:   [{permit1}]-- searcb for existings permits
# permit 2 issued.
# }

# app3 - submit a renewal - register -> update ApplicationRenewalHistory(application_type=EMERGEY, commet="AAA",application_user="X", process_name="C", historical_record={
# permits:   [{permit1, permit2}]-- search for existings permits
# permit issued.
# } Applying for permit 3 ( Details )


# app4 - submit a renewal - register -> update ApplicationRenewalHistory(application_type=EMERGEY, commet="AAA",application_user="X", process_name="C", historical_record={
# permits:   [{permit1, permit2, permit3}]-- search for existings permits
# permit issued.
# } Applying for permit 3 ( Details )


# 1. ApplicationRenewall - > ApplicationRenewalHistory.create ( historical_record( Permit object))

# event what triggers creation or update of historical records..[signals -> ]
