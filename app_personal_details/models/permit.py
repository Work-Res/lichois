from django.db import models

from dataclasses import dataclass
from datetime import date

from app.choices import APPLICANT_TYPE
from app.models import ApplicationBaseModel


@dataclass
class PermitData:
    permit_type: str
    permit_no: str
    date_issued: date
    date_expiry: date
    place_issue: str
    document_number: str


class Permit(ApplicationBaseModel):

    parent_object_id = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        help_text="Parent ID primary key.",
    )
    parent_object_type = models.CharField(max_length=200, null=True, blank=True)

    permit_type = models.CharField(max_length=190)
    permit_no = models.CharField(max_length=190)
    date_issued = models.DateField()
    date_expiry = models.DateField(null=True, blank=True)
    place_issue = models.CharField(max_length=190)
    security_number = models.CharField(max_length=190)
    applicant_type = models.CharField(
        max_length=200,
        choices=APPLICANT_TYPE,
        default="applicant",
    )
    generated_pdf = models.FileField(upload_to="generated/", null=True, blank=True)

    def to_dataclass(self) -> PermitData:
        return PermitData(
            permit_type=self.permit_type,
            permit_no=self.permit_no,
            date_issued=self.date_issued,
            date_expiry=self.date_expiry,
            place_issue=self.place_issue,
            document_number=self.document_number,
        )

    @classmethod
    def from_dataclass(cls, data: PermitData):
        return cls(
            permit_type=data.permit_type,
            permit_no=data.permit_no,
            date_issued=data.date_issued,
            date_expiry=data.date_expiry,
            place_issue=data.place_issue,
            document_number=data.document_number,
        )

    class Meta:
        verbose_name = "Permit"
