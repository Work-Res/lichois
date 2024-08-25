from django.test import TestCase

from ..service.email_receiver.oauth.token import get_oauth2_token


class TestToken(TestCase):

    def test_token(self):
        token = get_oauth2_token(
            "173d20ad-b66c-49f4-abf4-e18fafe84417",
            "5dm8Q~MJoDfJEAJIcIbWIbCA1akmtDVFyeSiGauM",
            "cad42c6a-07cb-4b36-88b3-aa1995b4e3ca",
        )
        print(token)
        self.assertIsNotNone(token)
