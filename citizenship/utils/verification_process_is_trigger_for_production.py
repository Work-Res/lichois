from citizenship.utils import CitizenshipProcessEnum


class VerificationProcessWhenCompletedIsRequiredForProduction:

    @staticmethod
    def configured_process():
        return [
            CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value,
            CitizenshipProcessEnum.PRESIDENT_POWER_10A.value
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
            CitizenshipProcessEnum.FOREIGN_SPOUSE_NATURALIZATION.value
        ]


class RecommendationDecisionProcessWhenCompletedIsRequiredForProduction:

    @staticmethod
    def configured_process():
        return [
            CitizenshipProcessEnum.ADOPTED_CHILD_REGISTRATION.value,
        ]
