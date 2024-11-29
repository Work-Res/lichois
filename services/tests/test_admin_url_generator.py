from django.http import Http404
from django.test import TestCase
from django.urls import reverse

from ..classes import AdminURLGenerator
from ..models import TestModel


class AdminURLGeneratorTest(TestCase):
    def setUp(self):
        
        # Create a sample Application object
        self.application = TestModel.objects.create(
            application_number='12345',
            # Add other required fields here
        )
        self.url_generator = AdminURLGenerator(TestModel)

    def test_get_add_url_without_next(self):
        url = self.url_generator.get_add_url()
        expected_url = reverse('admin:services_testmodel_add')
        self.assertEqual(url, expected_url)

    def test_get_add_url_with_next(self):
        next_url = '/admin/'
        url = self.url_generator.get_add_url(next_url=next_url)
        expected_url = f"{reverse('admin:services_testmodel_add')}?next={next_url}"
        self.assertEqual(url, expected_url)

    def test_get_change_url_without_next(self):
        url = self.url_generator.get_change_url(application_number='12345')
        expected_url = reverse('admin:services_testmodel_change', args=[self.application.pk])
        self.assertEqual(url, expected_url)

    def test_get_change_url_with_next(self):
        next_url = '/admin/'
        url = self.url_generator.get_change_url(application_number='12345', next_url=next_url)
        expected_url = f"{reverse('admin:services_testmodel_change', args=[self.application.pk])}?next={next_url}"
        self.assertEqual(url, expected_url)

    def test_get_change_url_object_does_not_exist(self):
        with self.assertRaises(Http404):
            self.url_generator.get_change_url(application_number='nonexistent')
