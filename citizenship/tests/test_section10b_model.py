from .base_setup import BaseSetup
from app.api import NewApplicationDTO
from app.models import Application
from app.classes import ApplicationService
from citizenship.models.section10b_decisions import Section10bApplicationDecisions
from ..utils import CitizenshipProcessEnum
from app.utils import ApplicationStatusEnum, ApplicationDecisionEnum


class Section10bApplicationDecisionsTestCase(BaseSetup):

    def setUp(self):
        super().setUp()
        # Create a sample Application instance
        self.defaults = {
            'mlha_director_decision': ApplicationDecisionEnum.PENDING.value,
            'deputy_ps_decision': ApplicationDecisionEnum.PENDING.value,
            'ps_decision': ApplicationDecisionEnum.PENDING.value,
            'president_ps_decision': ApplicationDecisionEnum.PENDING.value,
            'president_decision': ApplicationDecisionEnum.PENDING.value,
        }

        def create_new_application(self):
            self.new_application_dto = NewApplicationDTO(
                process_name=CitizenshipProcessEnum.PRESIDENT_POWER_10B.value,
                applicant_identifier='317918515',
                status=ApplicationStatusEnum.VERIFICATION.value,
                dob="06101990",
                work_place="01",
                application_type=CitizenshipProcessEnum.PRESIDENT_POWER_10B.value,
                full_name="Test test",
                applicant_type="student"
            )

        self.application_service = ApplicationService(
            new_application_dto=self.new_application_dto)
        return self.application_service.create_application()



    def test_create_decision(self):
        """Test creating a Section10bApplicationDecisions instance."""
        app = Application.objects.get(
            application_document__document_number=self.document_number)

        self.section10b_decisions = Section10bApplicationDecisions.objects.create(
            application=app,
           **self.defaults
        )

        self.assertIsInstance(self.section10b_decisions, Section10bApplicationDecisions)
        self.assertEqual(str(self.section10b_decisions), "Section 10B Application Decision")

    def test_partial_update_decision(self):
        """Test partially updating a Section10bApplicationDecisions instance."""
        app = Application.objects.get(
            application_document__document_number=self.document_number)

        self.section10b_decisions = Section10bApplicationDecisions.objects.create(
            application=app,
           **self.defaults
        )
        self.section10b_decisions.mlha_director_decision = ApplicationDecisionEnum.ACCEPTED.value
        self.section10b_decisions.save()

        updated_decision = Section10bApplicationDecisions.objects.get(application=app)
        self.assertEqual(updated_decision.mlha_director_decision, ApplicationDecisionEnum.ACCEPTED.value)

    def test_full_update_decision(self):
        """Test fully updating a Section10bApplicationDecisions instance."""

        app = Application.objects.get(
            application_document__document_number=self.document_number)

        self.section10b_decisions = Section10bApplicationDecisions.objects.create(
            application=app,
           **self.defaults
        )

        self.section10b_decisions.mlha_director_decision = ApplicationDecisionEnum.APPROVED.value
        self.section10b_decisions.deputy_ps_decision = ApplicationDecisionEnum.APPROVED.value
        self.section10b_decisions.ps_decision = ApplicationDecisionEnum.APPROVED.value
        self.section10b_decisions.president_ps_decision = ApplicationDecisionEnum.APPROVED.value
        self.section10b_decisions.president_decision = ApplicationDecisionEnum.APPROVED.value
        self.section10b_decisions.save()

        updated_decision = Section10bApplicationDecisions.objects.get(application=app)
        self.assertEqual(updated_decision.mlha_director_decision, ApplicationDecisionEnum.APPROVED.value)
        self.assertEqual(updated_decision.deputy_ps_decision, ApplicationDecisionEnum.APPROVED.value)
        self.assertEqual(updated_decision.ps_decision, ApplicationDecisionEnum.APPROVED.value)
        self.assertEqual(updated_decision.president_ps_decision, ApplicationDecisionEnum.APPROVED.value)
        self.assertEqual(updated_decision.president_decision, ApplicationDecisionEnum.APPROVED.value)

    def test_delete_decision(self):
        """Test deleting a Section10bApplicationDecisions instance."""

        app = Application.objects.get(
            application_document__document_number=self.document_number)

        self.section10b_decisions = Section10bApplicationDecisions.objects.create(
            application=app,
           **self.defaults
        )
        self.section10b_decisions.delete()
        with self.assertRaises(Section10bApplicationDecisions.DoesNotExist):
            Section10bApplicationDecisions.objects.get(application=app)