from abc import ABC, abstractmethod


class ModelRepositoryInterface(ABC):
    @abstractmethod
    def get_or_create(self, **kwargs):
        pass


class ModelRepository(ModelRepositoryInterface):
    def __init__(self, model_cls):
        self.model_cls = model_cls

    def get_or_create(self, **kwargs):
        return self.model_cls.objects.get_or_create(**kwargs)
