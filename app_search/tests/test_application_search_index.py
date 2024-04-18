import pytest
import random

from app.classes import CreateNewApplication
from app.api import NewApplication
from app.models import ApplicationStatus, ApplicationVersion
from app.utils.data import statuses

from haystack.query import SearchQuerySet

pytestmark = pytest.mark.django_db


class TestApplicationVersionIndex:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.new_app = NewApplication(process_name='residentpermit',
                                      applicant_identifier='31791851{}'.format(random.randint(2, 10)), status='new')
        self.create_new = CreateNewApplication(new_application=self.new_app)

        for status in statuses:
            ApplicationStatus.objects.create(
                **status
            )

    def test_indexing(self):
        create_new = CreateNewApplication(new_application=self.new_app)
        create_new.create()
        # Verify that objects are indexed
        sqs = SearchQuerySet().models(ApplicationVersion)
        app_v = sqs.all().count()
        assert sqs is not None
        self.assertEqual(app_v, 3)

        # self.assertIn("Test Object 1", [result.name for result in sqs])
        # self.assertIn("Test Object 2", [result.name for result in sqs])

    # def test_querying(self):
    #     # Test search query
    #     sqs = SearchQuerySet().models(ApplicationVersion).filter(name="Test Object 1")
    #     self.assertEqual(len(sqs), 1)
    #     self.assertEqual(sqs[0].description, "Description 1")
