from django.test import TestCase

from ..classes import PrePupolation


class TestPrepupolation(TestCase):

    def test_get_configuration(self):
        pre = PrePupolation()
        pre.configuration()

