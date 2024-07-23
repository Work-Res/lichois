from app.models import Application


class ApplicationEligibilityValidator:

    def __init__(self, document_number):
        self.document_number = document_number

    def application(self):
        try:
            Application.objects.get(application_document__document_number=self.document_number)
        except Application.DoesNotExist:
            pass

    @staticmethod
    def is_valid(self):
        application = self.application()
        if not application.batched and self.has_completed_assessment():
            return True
        return False

    def has_completed_assessment(self):
        return False
