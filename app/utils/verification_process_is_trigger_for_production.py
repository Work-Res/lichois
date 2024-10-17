from workresidentpermit.utils.work_resident_permit_application_type_enum import (
    WorkResidentPermitApplicationTypeEnum,
)
from .system_enums import ApplicationProcesses
from citizenship.utils import CitizenshipProcessEnum


class VerificationProcessWhenCompletedIsRequiredForProduction:

    @staticmethod
    def configured_process():
        return [
            CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value,
            CitizenshipProcessEnum.PRESIDENT_POWER_10A.value,
            ApplicationProcesses.BLUE_CARD_RETURNS.value,
            WorkResidentPermitApplicationTypeEnum.WORK_RESIDENT_PERMIT_ONLY.value,
        ]


class MinisterProcessWhenCompletedIsRequiredForProduction:

    @staticmethod
    def configured_process():
        return [
            CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value,
            CitizenshipProcessEnum.UNDER_20_CITIZENSHIP.value,
            CitizenshipProcessEnum.DOUBT_CITIZENSHIP_CERTIFICATE.value,
            CitizenshipProcessEnum.CITIZENSHIP_RESUMPTION.value,
            CitizenshipProcessEnum.SETTLEMENT.value,
            CitizenshipProcessEnum.NATURALIZATION.value,
            CitizenshipProcessEnum.FOREIGN_SPOUSE_NATURALIZATION.value,
            CitizenshipProcessEnum.DUAL_RENUNCIATION.value,
            CitizenshipProcessEnum.ADOPTED_CHILD_REGISTRATION.value,
        ]


class RecommendationDecisionProcessWhenCompletedIsRequiredForProduction:

    @staticmethod
    def configured_process():
        return [
            CitizenshipProcessEnum.ADOPTED_CHILD_REGISTRATION.value,
        ]


class PresidentProcessWhenCompletedIsRequiredForProduction:

    @staticmethod
    def configured_process():
        return [
            CitizenshipProcessEnum.PRESIDENT_POWER_10B.value,
        ]
