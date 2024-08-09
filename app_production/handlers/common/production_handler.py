from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app_production.services.document import WordDocumentTemplateService

T = TypeVar("T")
S = TypeVar("S")


class ProductionHandler(ABC, Generic[T, S]):

    @abstractmethod
    def execute(self, config_cls: T, production_context: S) -> None:
        """
        Execute handler actions.

        :param config_cls: Production Config class
        :param production_context: Production Context Class
        :raises ProductionProcessException: on error
        """
        document = WordDocumentTemplateService(template_path=config_cls.template_path)

        document.replace_placeholders(context=production_context.context())
        document.save_document(document, config_cls.document_output_path)
