from django.test import TestCase

import os
import django
from django.apps import apps



class TestPersonalDetails(TestCase):

    def list_models_and_fields(app_label):
        try:
            app_config = apps.get_app_config(app_label)
        except LookupError:
            print(f"No app with label '{app_label}' found.")
            return

        models = app_config.get_models()

        for model in models:
            print(f"Model: {model.__name__}")
            fields = model._meta.get_fields()
            for field in fields:
                print(f"{app_label}_{model.__name__}_{field.name}")
            print()

    def test_fields_names(self):
        self.list_models_and_fields("app_personal_details")



