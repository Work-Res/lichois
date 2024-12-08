from django.http import Http404
from django.test import TestCase
from django.urls import reverse
from urllib.parse import unquote

from ..classes import AdminURLGenerator
from ..models import TestModel






class AdminURLGeneratorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model = TestModel
        cls.obj = TestModel.objects.create(
            application_number="APP12345",
            non_citizen_identifier="NC12345"
        )
        cls.generator = AdminURLGenerator(cls.model)

    def test_get_add_url_with_non_citizenship_identifier(self):
        url = self.generator.get_add_url(non_citizen_identifier="NC12345")
        expected_url = reverse(f"admin:{self.obj._meta.app_label}_{self.obj._meta.model_name}_add")
        self.assertIn(f"non_citizen_identifier=NC12345", url)
        self.assertTrue(url.startswith(expected_url))

    def test_get_add_url_without_non_citizenship_identifier(self):
        url = self.generator.get_add_url()
        expected_url = reverse(f"admin:{self.obj._meta.app_label}_{self.obj._meta.model_name}_add")
        self.assertEqual(url, expected_url)

    def test_get_change_url_with_application_number(self):
        url = self.generator.get_change_url(application_number="APP12345")
        expected_url = reverse(
            f"admin:{self.obj._meta.app_label}_{self.obj._meta.model_name}_change", args=[self.obj.pk]
        )
        self.assertEqual(url, expected_url)

    def test_get_change_url_with_non_citizenship_identifier(self):
        url = self.generator.get_change_url(non_citizen_identifier="NC12345")
        expected_url = reverse(
            f"admin:{self.obj._meta.app_label}_{self.obj._meta.model_name}_change", args=[self.obj.pk]
        )
        self.assertEqual(url, expected_url)

    def test_get_change_url_with_invalid_application_number(self):
        with self.assertRaises(Http404):
            self.generator.get_change_url(application_number="INVALID_APP")

    def test_get_change_url_with_invalid_non_citizenship_identifier(self):
        with self.assertRaises(Http404):
            self.generator.get_change_url(non_citizen_identifier="INVALID_NC")

    def test_get_change_url_without_identifiers(self):
        with self.assertRaises(ValueError):
            self.generator.get_change_url()

    def test_get_add_url_with_additional_query_params(self):
        url = self.generator.get_add_url(non_citizen_identifier="NC12345", next="/redirect/")
        url = unquote(url)
        self.assertIn("non_citizen_identifier=NC12345", url)
        self.assertIn("next=/redirect/", url)

    def test_get_change_url_with_additional_query_params(self):
        url = self.generator.get_change_url(application_number="APP12345", next="/redirect/")
        url = unquote(url)
        self.assertIn("next=/redirect/", url)
