from citizenship.utils import CitizenshipProcessEnum


class VerificationProcessWhenCompletedIsRequiredForProduction:

    @staticmethod
    def configured_process():
        return [
            CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value
        ]
