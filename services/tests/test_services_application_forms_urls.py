from django.urls import reverse
from django.test import TestCase
from unittest.mock import MagicMock, patch
from ..classes import AdminURLGenerator, ServicesApplicationFormsUrls


class ServicesApplicationFormsUrlsTest(TestCase):
    def setUp(self):
        self.document_number = '12345'
        self.next_url = 'some-next-url'
        self.mock_model = MagicMock()
        self.mock_model.__name__ = 'MockModel'
        self.mock_admin_url_generator = patch('services_application_forms_urls.AdminURLGenerator', autospec=True).start()
        
    def tearDown(self):
        patch.stopall()

    def test_application_urls_object_exists(self):
        # Mocking model instance retrieval
        mock_instance = MagicMock()
        self.mock_model.objects.get.return_value = mock_instance

        # Mock change URL
        mock_change_url = 'mock/change/url'
        self.mock_admin_url_generator.return_value.get_change_url.return_value = mock_change_url

        # Initialize the class
        service_urls = ServicesApplicationFormsUrls(
            document_number=self.document_number,
            application_models_cls=[self.mock_model],
            next_url=self.next_url
        )
        urls = service_urls.application_urls()

        # Assertions
        self.mock_model.objects.get.assert_called_once_with(document_number=self.application_number)
        self.mock_admin_url_generator.return_value.get_change_url.assert_called_once_with(
            self.document_number, next_url=reverse(self.next_url)
        )
        self.assertEqual(urls['MockModel'], [mock_change_url, mock_instance])

    def test_application_urls_object_does_not_exist(self):
        # Mocking model instance retrieval failure
        self.mock_model.objects.get.side_effect = self.mock_model.DoesNotExist

        # Mock add URL
        mock_add_url = 'mock/add/url'
        self.mock_admin_url_generator.return_value.get_add_url.return_value = mock_add_url

        # Initialize the class
        service_urls = ServicesApplicationFormsUrls(
            document_number=self.document_number,
            application_models_cls=[self.mock_model],
            next_url=self.next_url
        )
        urls = service_urls.application_urls()

        # Assertions
        self.mock_model.objects.get.assert_called_once_with(document_number=self.application_number)
        self.mock_admin_url_generator.return_value.get_add_url.assert_called_once_with(
            next_url=reverse(self.next_url)
        )
        self.assertEqual(urls['MockModel'], [mock_add_url, None])

    def test_application_urls_no_models(self):
        # Initialize the class with no models
        service_urls = ServicesApplicationFormsUrls(
            document_number=self.document_number,
            application_models_cls=[],
            next_url=self.next_url
        )
        urls = service_urls.application_urls()

        # Assertions
        self.assertEqual(urls, {})

    def test_application_urls_none_next_url(self):
        # Mocking model instance retrieval
        mock_instance = MagicMock()
        self.mock_model.objects.get.return_value = mock_instance

        # Mock change URL
        mock_change_url = 'mock/change/url'
        self.mock_admin_url_generator.return_value.get_change_url.return_value = mock_change_url

        # Initialize the class without next_url
        service_urls = ServicesApplicationFormsUrls(
            document_number=self.document_number,
            application_models_cls=[self.mock_model],
            next_url=None
        )
        urls = service_urls.application_urls()

        # Assertions
        self.mock_model.objects.get.assert_called_once_with(document_number=self.application_number)
        self.mock_admin_url_generator.return_value.get_change_url.assert_called_once_with(
            self.document_number, next_url=None
        )
        self.assertEqual(urls['MockModel'], [mock_change_url, mock_instance])
