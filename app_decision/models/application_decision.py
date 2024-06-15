
from django.db import models

from app.models import ApplicationBaseModel

from .application_decision_type import ApplicationDecisionType
from app_comments.models import Comment


class ApplicationDecision(ApplicationBaseModel):

    final_decision_type = models.ForeignKey(ApplicationDecisionType, on_delete=models.CASCADE,
                                            related_name='final_decision_type', null=True, blank=True)

    proposed_decision_type = models.ForeignKey(ApplicationDecisionType, on_delete=models.CASCADE,
                                               related_name='proposed_decision_type', null=True, blank=True)

    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Application Decision"
        ordering = ['-created']

# Permit model
# ApplicationDecision

# TypeError: Object of type Person is not JSON serializable

# from app_personal_details.models import Permit, Person
# from app.models import Application
# from datetime import date
#
# apps = Application.objects.all()[20:22]
# application_status = ApplicationStatus.objects.get(code__iexact='Accepted')
# accepted = ApplicationDecisionType.objects.get(id='1745ceeb-3b5a-4e4a-b499-73593068ac9d')
# i = 0
# for app in apps:
#     app.application_status = application_status
#     app.save()
#     i = i + 1
#     Permit.objects.create(
#         permit_type='WORK_RESIDENT_ONLY', permit_no=f'300000001{i}',
#         date_issued=date(2024,6 , 20),date_expiry=date(2025, 6, 1),
#         place_issue='Gaborone', security_number=f'000000001123{i}',
#         document_number=app.application_document.document_number)
#     ApplicationDecision.objects.create(
#         proposed_decision_type=accepted,
#         document_number=app.application_document.document_number
#     )