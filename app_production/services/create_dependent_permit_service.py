from app_personal_details.models import Spouse


class CreateDependentPermitService:

    def create_spouse_permit(self, document_number):
        try:
            spouses = Spouse.objects.get(
                document_number=document_number
            )
        except Spouse.DoesNotExists:
            pass

    def create_child_permit(self, document_number):
        pass