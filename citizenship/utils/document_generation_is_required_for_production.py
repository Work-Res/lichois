from citizenship.utils import CitizenshipProcessEnum


class CitizenshipDocumentGenerationIsRequiredForProduction:

    @staticmethod
    def configured_process():
        return [
            'MATURITY_PERIOD_WAIVER',
           CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value
        ]
