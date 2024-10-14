from citizenship.utils import CitizenshipProcessEnum


class CitizenshipDocumentGenerationIsRequiredForProduction:

    @staticmethod
    def configured_process():
        return [
            'MATURITY_PERIOD_WAIVER',
           CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value,
            CitizenshipProcessEnum.ADOPTED_CHILD_REGISTRATION.value,
            CitizenshipProcessEnum.UNDER_20_CITIZENSHIP.value
        ]
