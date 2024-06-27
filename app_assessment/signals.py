from django.dispatch import Signal

from app_assessment.classes import AssessmentHandler

run_assessment_calculation = Signal()


def run_assessment_calculation_handler(sender, source=None, rules=None,
                                       assessment_rules_file_location_name=None,
                                       document_number=None,
                                       **kwargs):
    evaluator = AssessmentHandler(
        assessment_rules_file_location_name=assessment_rules_file_location_name,
        source=source,
        document_number=document_number
    )
    evaluator.create_assessment_results()
