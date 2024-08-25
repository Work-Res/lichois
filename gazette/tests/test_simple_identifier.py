from datetime import date

from identifier.simple_identifier import SimpleIdentifier
from django.test import TestCase


class TestSimpleIdentifier(TestCase):

    def test_simple_identifier(self):
        today = date.today()
        date_string = today.strftime('%d%m%Y')
        simple = SimpleIdentifier(identifier_prefix="DB", address_code=date_string[-6:])
        print(simple.identifier)
        self.assertIsNotNone(simple.identifier)
