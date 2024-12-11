from django.http import Http404
from django.test import TestCase
from django.urls import reverse

from ..classes import AdminURLGenerator
from ..models import TestModel


class AdminURLGeneratorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test object
        cls.test_object = TestModel.objects.create(
            document_number='APP001',
            non_citizen_identifier='NCID001',
        )
        cls.generator_default = AdminURLGenerator(TestModel)  # Default admin site
        cls.generator_custom = AdminURLGenerator(TestModel, admin_site_name='services_admin')

    def test_get_add_url_services_admin(self):
        url = self.generator_custom.get_add_url(non_citizen_identifier='NCID001')
        expected_url = reverse('services_admin:services_testmodel_add') + '?non_citizen_identifier=NCID001'
        self.assertEqual(url, expected_url)

    def test_get_change_url_services_admin_with_application_number(self):
        url = self.generator_custom.get_change_url(document_number='APP001')
        expected_url = reverse('services_admin:services_testmodel_change', args=[self.test_object.pk])
        self.assertEqual(url, expected_url)

    def test_get_change_url_services_admin_with_non_citizen_identifier(self):
        url = self.generator_custom.get_change_url(non_citizen_identifier='NCID001')
        expected_url = reverse('services_admin:services_testmodel_change', args=[self.test_object.pk])
        self.assertEqual(url, expected_url)

    def test_get_change_url_raises_error_for_invalid_application_number(self):
        with self.assertRaises(Http404):
            self.generator_default.get_change_url(document_number='INVALID')

    def test_get_change_url_raises_error_for_invalid_non_citizen_identifier(self):
        with self.assertRaises(Http404):
            self.generator_custom.get_change_url(non_citizen_identifier='INVALID')

    def test_get_change_url_raises_value_error_when_no_identifiers(self):
        with self.assertRaises(ValueError):
            self.generator_default.get_change_url()

    def test_add_query_params(self):
        base_url = '/admin/services/testmodel/add/'
        query_params = {'key1': 'value1', 'key2': 'value2'}
        result = self.generator_default.add_query_params(base_url, query_params)
        expected_url = '/admin/services/testmodel/add/?key1=value1&key2=value2'
        self.assertEqual(result, expected_url)

    def test_add_query_params_no_params(self):
        base_url = '/admin/services/testmodel/add/'
        result = self.generator_default.add_query_params(base_url, {})
        self.assertEqual(result, base_url)
