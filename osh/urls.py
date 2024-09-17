from rest_framework.routers import DefaultRouter

from .views import (
    AccidentViewSet, ApplicantConstructionExperienceViewSet,
    ApplicantExperienceViewSet, ApplicantHoistLiftExperienceViewSet,
    AppointeeViewSet, AppointerViewSet, AppointmentViewSet,
    BearerViewSet, BoilerFittingViewSet, BoilerViewSet,
    CertificateViewSet, CompanyViewSet, DangerousOccurenceViewSet,
    DefectViewSet, EmployeeViewSet, EquipmentViewSet,ExaminationViewSet,
    ExaminerViewSet, FactoryViewSet, HeatTreatmentViewSet, InjuredPersonViewSet,
    InspectionViewSet, InspectorViewSet, LiftingApplianceViewSet,
    MedicalPractitionerViewSet, PersonViewSet, PremiseViewSet,
    QualificationViewSet, RefereeViewSet, ReinspectionViewSet, ReportViewSet,
    WitnessViewSet
)
from django.urls import path, include

router = DefaultRouter()

router.register(r"accident", AccidentViewSet)
router.register(r"applicantconstructionexperience", ApplicantConstructionExperienceViewSet)
router.register(r"applicantexperience", ApplicantExperienceViewSet)
router.register(r"applicanthoistliftexperience", ApplicantHoistLiftExperienceViewSet)
router.register(r"appointee", AppointeeViewSet)
router.register(r"appointer", AppointerViewSet)
router.register(r"appointment", AppointmentViewSet)
router.register(r"bearer", BearerViewSet)
router.register(r"boilerfitting", BoilerFittingViewSet)
router.register(r"boiler", BoilerViewSet)
router.register(r"certificate", CertificateViewSet)
router.register(r"company", CompanyViewSet)
router.register(r"dangerousoccurence", DangerousOccurenceViewSet)
router.register(r"defect", DefectViewSet)
router.register(r"employee", EmployeeViewSet)
router.register(r"equipment", EquipmentViewSet)
router.register(r"examination", ExaminationViewSet)
router.register(r"examiner", ExaminerViewSet)
router.register(r"factory", FactoryViewSet)
router.register(r"heattreatment", HeatTreatmentViewSet)
router.register(r"injuredperson", InjuredPersonViewSet)
router.register(r"inspection", InspectionViewSet)
router.register(r"inspector", InspectorViewSet)
router.register(r"liftingappliance", LiftingApplianceViewSet)
router.register(r"medicalpractitioner", MedicalPractitionerViewSet)
router.register(r"person", PersonViewSet)
router.register(r"premise", PremiseViewSet)
router.register(r"qualification", QualificationViewSet)
router.register(r"referee", RefereeViewSet)
router.register(r"reinspection", ReinspectionViewSet)
router.register(r"report", ReportViewSet)
router.register(r"witness", WitnessViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
