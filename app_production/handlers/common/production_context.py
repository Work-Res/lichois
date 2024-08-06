from abc import ABC, abstractmethod


class ProductionContext(ABC):

    @abstractmethod
    def context(self):
        pass


class GenericProductionContext(ProductionContext):

    def context(self):
        return {
            'placeholder1': 'value1',
            'placeholder2': 'value2',
        }
