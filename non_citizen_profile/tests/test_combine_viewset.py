from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, datetime
from ..models import Address, Biometrics, ContactDetails, Passport, PersonalDetails, Education, NextOfKin
from api.serializers import CombinedSerializer

class UserProfileTests(APITestCase):
    def setUp(self):
        # Create instances of each model
        self.address = Address.objects.create(
            non_citizen_id=1,
            country='Botswana',  
            city='Gaborone',
            street_address='Extension 2',
            address_type='P O Box',  
            status='active',  
            po_box='Test 123'
        )
        self.biometrics = Biometrics.objects.create(
            non_citizen_id=1,
            facial_image='https://familyguyaddicts.com/wp-content/uploads/2014/04/meg-animation-078idlepic4x.png',
            fingerprint=b'\x00\x01\x02\x03',  
            biometric_timestamp=datetime(2024, 8, 16, 12, 0, 0)  
        )
        self.contact_details = ContactDetails.objects.create(
            non_citizen_id=1,
            telephone='3602438',
            cellphone='71000111',
            alt_cellphone='72100011',
            email='test@test.com',
            alt_email='test1@test.com',
            emergency_contact_name='Test Test',
            emergency_contact_number='78112233'
        )
        self.passport = Passport.objects.create(
            non_citizen_id=1,
            passport_number='123456789',  
            date_issued=date(2024, 8, 12),  
            place_issued='Gaborone',
            expiry_date=date(2026, 8, 12),  
            nationality='Motswana',
            photo='https://familyguyaddicts.com/wp-content/uploads/2014/04/meg-animation-078idlepic4x.png',
        )
        self.personal_details = PersonalDetails.objects.create(
            non_citizen_id=1,
            first_name='Africort',
            middle_name='Investments',
            last_name='Test',
            maiden_name='Test',
            dob=date(2019, 6, 30),  
            occupation='Developer'
        )
        self.education = Education.objects.create(
            non_citizen_id=1,
            level='Bachelor\'s Degree',
            field_of_study='Computer Science',
            institution='University of Botswana',
            start_date=date(2015, 1, 1),
            end_date=date(2019, 12, 31)
        )
        self.next_of_kin = NextOfKin.objects.create(
            non_citizen_id=1,
            first_name='John',
            last_name='Doe',
            telephone='123456789',
            cell_phone='987654321',
            relation='Brother'
        )

        self.combined_url = '/combined/'  

    def test_combined_view_success(self):
        response = self.client.get(self.combined_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_data = CombinedSerializer({
            "address": self.address,
            "biometrics": self.biometrics,
            "contact_details": self.contact_details,
            "passport": self.passport,
            "personal_details": self.personal_details
        }).data

        self.assertEqual(response.data, expected_data)

    def test_combined_view_not_found(self):
        # Delete or omit one of the objects
        self.personal_details.delete()
        response = self.client.get(self.combined_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'One or more resources not found.')
