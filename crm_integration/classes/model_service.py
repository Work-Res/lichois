# model_services.py
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from ..api.serializers import create_model_serializer
from .model_repository import ModelRepositoryInterface


class ModelService:
    def __init__(self, repository: ModelRepositoryInterface):
        self.repository = repository

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
                print(f"Instance created: {instance.__dict__}")

            for field_name, field_value in validated_data.items():
                setattr(instance, field_name, field_value)
            try:
                with transaction.atomic():
                    instance.full_clean()
                    instance.save()
                    print(f"Instance saved: {instance}")
            except ValidationError as e:
                print(f"Validation error: {e}")
                raise
            except IntegrityError as e:
                print(f"Integrity error (likely due to NOT NULL constraint): {e}")
                raise
            except Exception as e:
                print(f"Error saving instance: {e}")
                raise
            return instance, created
        else:
            raise ValueError(serializer.errors)
