from django.dispatch import Signal
from datetime import date

from app_assessment.classes import AssessmentEvaluator
from app_assessment.models import AssessmentResult

run_assessment_calculation = Signal()


def run_assessment_calculation_handler(sender, source=None, rules=None,  **kwargs):
    assessment_evaluator = AssessmentEvaluator(source, rules)
    assessment_evaluator.evaluate()
    AssessmentResult.objects.create(
        document_number=sender.application_document.document_number,
        score=assessment_evaluator.calculate_score(),
        output_results=assessment_evaluator.assessment_results,
        result_date=date.today()
    )
