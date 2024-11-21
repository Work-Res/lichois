from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from app_address.models import ApplicationAddress
from app_personal_details.models import Permit

from .document_context_generator import DocumentContextGenerator


class WorkAndResidentLetterContextGenerator(DocumentContextGenerator):

    def format_date_with_suffix(self, date):

        day = date.day

        if 10 <= day & 100 <= 20:
            suffix = 'th'
        else:
            suffix ={1: 'st', 2: 'nd', 3:'rd'}.get(day%10, 'th')
        return date.strftime(f"%d{suffix} %B %Y")

    def generate(self, application):
        document_number = application.application_document.document_number
        document_date = self.format_date_with_suffix(application.application_document.document_date)
        years = datetime.now() + relativedelta(months=30)
        context = {
            'document_type': 'work_and_residence',
            'document_number': document_number,
            'permit_number': self.permit_info(document_number=document_number),
            'document_date': document_date,
            'reference_number': document_number,
            'today_date': date.today().strftime("%Y-%m-%d"),
            'applicant_fullname': application.full_name(),
            'salutation': 'Sir/Madam',
            'end_date': years.strftime("%Y-%m-%d"),
            'start_date': datetime.now().strftime("%Y-%m-%d"),
            'officer_fullname': self.officer(),
            'position': 'Minister',
            'officer_contact_information': '',
            'applicant_address': self.applicant_address(application),
            'decision_date': date.today().strftime("%Y-%m-%d"),
            'application_type': application.application_type.replace("_", " "),
            'officer_location': 'Head Office'
        }
        return context

    def applicant_address(self, application):
        try:
            # Use select_related to optimize the query by fetching related objects in one go
            application_address = ApplicationAddress.objects.select_related('country').get(
                document_number=application.application_document.document_number
            )

            # Format the address components
            address_parts = [
                application_address.private_bag or '',
                application_address.po_box or '',
                application_address.street_address or '',
                # application_address.country.code if application_address.country else ''
            ]

            # Join the non-empty parts with proper spacing
            full_address = ' '.join(part for part in address_parts if part)

            return full_address or 'Address not available'

        except ApplicationAddress.DoesNotExist:
            # Handle case where the address is not found
            return 'Address not available'

    def officer(self):
        return 'Ana Mokgethi'

    def permit_info(self, document_number):
        try:
            permit = Permit.objects.get(
                document_number=document_number,
                applicant_type='applicant'
            )
            return permit.permit_no
        except Permit.DoesNotExist:
            return ''
