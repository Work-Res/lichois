from django.test import TestCase

from .classes import CrmRequestHandler


class GroupAndTrimKeysTests(TestCase):

    def setUp(self):

        self.main_dict = {
            "app_personal_details_Passport_photo": None,
            "app_personal_details_Person_last_name": None,
            "workresidentpermit_Residence_Permit_current_nationality": None,
            "workresidentpermit_Residence_Permit_previous_nationality": None,
            "workresidentpermit_Spouse_last_name": None,
            "workresidentpermit_Spouse_first_name": None,
            "placeholder": None  # Should not match any substring
        }

        # Substrings to match
        self.substrings = [
            "app_personal_details_passport",
            "workresidentpermit_Residence_Permit",
            "workresidentpermit_Spouse"
        ]
        self.crm_request = CrmRequestHandler(
            crm_request=self.main_dict)

    def test_group_and_trim_keys(self):

        result = self.crm_request.group_and_trim_keys()


        expected_result = [
            {
                "app_personal_details": {
                    "Passport_photo": None,
                    "Person_last_name": None
                }
            },
            {
                "workresidentpermit_Residence_Permit": {
                    "current_nationality": None,
                    "previous_nationality": None
                }
            },
            {
                "workresidentpermit_Spouse": {
                    "last_name": None,
                    "first_name": None
                }
            }
        ]

        # Assert that the result matches the expected output
        self.assertEqual(result, expected_result)

