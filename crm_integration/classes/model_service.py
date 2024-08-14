# model_services.py
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from ..api.serializers import create_model_serializer
from .model_repository import ModelRepositoryInterface
import logging


class ModelService:
    def __init__(self, repository: ModelRepositoryInterface):
        self.repository = repository
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def process_data(self, data):
        serializer = create_model_serializer(self.repository.model_cls)(data=data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            unique_field = validated_data.get(
                "email"
            )  # Replace "email" with your unique field
            if unique_field:
                instance, created = self.repository.get_or_create(
                    email=unique_field, defaults=validated_data
                )
            else:
                instance = self.repository.model_cls(**validated_data)
                created = True

            for field_name, field_value in validated_data.items():
                setattr(instance, field_name, field_value)
            try:
                with transaction.atomic():
                    instance.full_clean()
                    instance.save()
            except ValidationError as e:
                print(f"Validation error: {e}")
                self.logger.error(f"Validation error: {e}")
                raise ValueError(f"Validation error: {e}")
            except IntegrityError as e:
                self.logger.error(
                    f"Integrity error (likely due to NOT NULL constraint): {e}"
                )
                raise ValueError(f"Integrity error: {e}")
            except Exception as e:
                self.logger.error(f"Error saving instance: {e}")
                raise ValueError(f"Error saving instance: {e}")
            return instance, created
        else:
            self.logger.error(serializer.errors)
            raise ValueError(serializer.errors)
