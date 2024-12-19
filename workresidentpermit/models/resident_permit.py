from django.db import models
from app.models import ApplicationBaseModel
from base_module.choices import PREFERRED_METHOD_COMM, YES_NO, REASONS_PERMIT


class ResidencePermit(ApplicationBaseModel):
    language = models.CharField(
        max_length=190,
        verbose_name="Languages applicant is able to read and write: "
    )
    permit_reason = models.TextField(
        verbose_name="Give reasons for applying for a permit"
    )
    previous_nationality = models.CharField(
        max_length=190,
        verbose_name="Previous nationality(State name of country)",
    )
    current_nationality = models.CharField(
        max_length=190,
        verbose_name="Current nationality(State name of country)",
    )
    state_period_required = models.DateField(
        verbose_name="State until when the period is required."
    )
    propose_work_employment = models.CharField(
        max_length=4,
        choices=YES_NO,
        verbose_name=(
            "Do you propose to take up employment or engage for reward in any business, "
            "profession, or other occupation in Botswana? "
            "If yes, please complete the application for a work permit and attach it to this form."
        ))
    reason_applying_permit = models.CharField(
        max_length=190,
        null=True,
        choices=REASONS_PERMIT,
        blank=True,
        verbose_name="If you do not propose to take up paid employment or engage "
        "for reward in any business, profession or other occupation "
        "in Botswana, what are your reasons for applying for a "
        "residence permit?",
    )
    documentary_proof = models.CharField(
        max_length=190,
        verbose_name="State how intend to support yourself and dependent(if any)."
                     "Give full details supported by documentary proof: "
    )
    travelled_on_pass = models.CharField(
        max_length=190,
        verbose_name="Have you ever travelled on the passports of any of those countries? If so, give particulars: ",
    )
    is_spouse_applying_residence = models.CharField(
        max_length=190,
        choices=YES_NO,
        verbose_name="Is your spouse applying for residence in Botswana?",
    )
    ever_prohibited = models.TextField(
        verbose_name="Have you or those accompanying you ever been ordered to leave"
                     "or prohibited from entering Botswana or any Other country?"
                     "If so, give particulars: ",
    )
    sentenced_before = models.TextField(
        verbose_name="Have you or those accompanying you ever been ordered been sentenced in any country to any period"
                     "imprisonment either without the option or in default of payment of a fine(whether or such"
                     "fine was suspected), or to any sentence for an offence involving violence,"
                     "dishonesty or non-payment of any tax or duty?"
                     "If so, give particulars: ",
    )
    entry_place = models.CharField(
        max_length=190,
        verbose_name="Place of entry in Botswana"
    )
    arrival_date = models.DateField(
        verbose_name="Date of arrival in Botswana"
    )
    preferred_method_comm = models.CharField(
        max_length=190,
        choices=PREFERRED_METHOD_COMM,
        null=True,
        blank=True,
        verbose_name="Preferred method of communication",
    )
    preferred_method_comm_value = models.CharField(
        max_length=190,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Residence Permits"
